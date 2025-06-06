# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
from datetime import datetime, timedelta
from io import StringIO
from operator import attrgetter

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round


class AbcClassificationProfile(models.Model):

    _inherit = "abc.classification.profile"

    profile_type = fields.Selection(
        selection_add=[
            (
                "sale_stock",
                "Based on the count of delivered sale order line by product",
            ),
            (
                "product_cost", 
                "Based on product cost",
            )
        ],
        ondelete={
            "sale_stock": "cascade",
            "product_cost": "cascade",
        },
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
        ondelete="cascade",
        default=lambda self: self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.user.company_id.id)], limit=1
        ),
    )

    @api.constrains("profile_type", "warehouse_id")
    def _check_warehouse_id(self):
        for rec in self:
            if rec.profile_type == "sale_stock" and not rec.warehouse_id:
                raise ValidationError(
                    _("You must specify a warehouse for {profile_name}").format(
                        profile_name=rec.name
                    )
                )

    @api.model
    def _get_collected_data_class(self):
        if self.profile_type == "product_cost":
            return ProductCostData
        return SaleStockData

    def _init_collected_data_instance(self):
        self.ensure_one()
        data_class = self._get_collected_data_class()()
        data_class.profile = self
        return data_class

    def _get_all_product_ids(self):
        """Get a set of product ids with the current profile"""
        self.ensure_one()
        self.env.cr.execute(
            """
            SELECT
                abc_rel.product_id
            FROM
                abc_classification_profile_product_rel abc_rel
            JOIN
                product_product pp
                ON pp.id = abc_rel.product_id
            WHERE
                pp.active
                AND abc_rel.profile_id = %(profile_id)s
        """,
            {"profile_id": self.id},
        )
        return {r[0] for r in self.env.cr.fetchall()}

    def _get_sale_stock_data_query(self, from_date, customer_location_ids):
        query = """
            SELECT
                sol.product_id product_id,
                COUNT(sol.id) number_so_lines
            FROM
                sale_order so
            JOIN
                sale_order_line sol ON
                sol.order_id = so.id
            JOIN
                abc_classification_profile_product_rel rel
                ON rel.product_id = sol.product_id
            JOIN
                product_product pp
                ON pp.id = sol.product_id
            WHERE sol.qty_delivered > 0
                AND pp.active
                AND rel.profile_id = %(profile_id)s
                AND so.warehouse_id = %(current_warehouse_id)s
            AND EXISTS (
                    SELECT
                        1
                    FROM
                        stock_move sm
                    WHERE
                        sm.date > %(start_date)s
                        AND sm.location_dest_id in %(customer_loc_ids)s
                        AND sm.sale_line_id = sol.id
                )

            GROUP BY sol.product_id
            ORDER BY number_so_lines DESC
        """
        params = {
            "start_date": from_date,
            "current_warehouse_id": self.warehouse_id.id,
            "profile_id": self.id,
            "customer_loc_ids": tuple(customer_location_ids),
        }
        return query, params

    def _get_product_cost_data_query(self):
        """Get product cost data for ABC classification"""
        query = """
            SELECT
                pp.id as product_id,
                pt.standard_price as product_cost
            FROM
                product_product pp
            JOIN
                product_template pt ON pp.product_tmpl_id = pt.id
            JOIN
                abc_classification_profile_product_rel rel ON rel.product_id = pp.id
            WHERE
                pp.active
                AND rel.profile_id = %(profile_id)s
            ORDER BY pt.standard_price DESC
        """
        params = {
            "profile_id": self.id,
        }
        return query, params

    def _get_data(self, from_date=None):
        """Get a list of statics info from the DB ordered by relevant metric"""
        self.ensure_one()
        
        if self.profile_type == "product_cost":
            return self._get_product_cost_data()
        else:
            return self._get_sale_stock_data(from_date)

    def _get_product_cost_data(self):
        """Get product cost data for ABC classification"""
        self.ensure_one()
        to_date = datetime.today()
        from_date = fields.Datetime.to_string(
            datetime.today() - timedelta(days=self.period)
        )
        
        # Collect all products linked to the profile
        all_product_ids = self._get_all_product_ids()

        # Get product costs
        query, params = self._get_product_cost_data_query()
        self.env.cr.execute(query, params)
        result = self.env.cr.fetchall()

        total_cost = 0
        product_cost_data_list = []
        ranking = 1
        ProductProduct = self.env["product.product"]
        
        for r in result:
            product_cost_data = self._init_collected_data_instance()
            product_id = r[0]
            product_cost_data.product = ProductProduct.browse(product_id)
            product_cost_data.product_cost = float(r[1]) if r[1] else 0.0
            product_cost_data.ranking = ranking
            product_cost_data.from_date = from_date
            product_cost_data.to_date = to_date
            ranking += 1
            total_cost += product_cost_data.product_cost
            product_cost_data_list.append(product_cost_data)
            all_product_ids.remove(product_id)

        # Add products with zero cost
        for product_id in all_product_ids:
            product_cost_data = self._init_collected_data_instance()
            product_cost_data.product = ProductProduct.browse(product_id)
            product_cost_data.product_cost = 0.0
            product_cost_data.ranking = ranking
            product_cost_data.from_date = from_date
            product_cost_data.to_date = to_date
            product_cost_data_list.append(product_cost_data)

        return product_cost_data_list, total_cost

    def _get_sale_stock_data(self, from_date):
        """Original sale stock data collection method"""
        self.ensure_one()
        from_date = (
            from_date
            if from_date
            else fields.Datetime.to_string(
                datetime.today() - timedelta(days=self.period)
            )
        )
        to_date = datetime.today()
        customer_location_ids = (
            self.env["stock.location"].search([("usage", "=", "customer")]).ids
        )
        all_product_ids = self._get_all_product_ids()

        query, params = self._get_sale_stock_data_query(
            from_date, customer_location_ids
        )
        self.env.cr.execute(query, params)
        result = self.env.cr.fetchall()

        total = 0
        sale_stock_data_list = []
        ranking = 1
        ProductProduct = self.env["product.product"]
        for r in result:
            sale_stock_data = self._init_collected_data_instance()
            product_id = r[0]
            sale_stock_data.product = ProductProduct.browse(product_id)
            sale_stock_data.number_so_lines = int(r[1])
            sale_stock_data.ranking = ranking
            sale_stock_data.from_date = from_date
            sale_stock_data.to_date = to_date
            ranking += 1
            total += int(r[1])
            sale_stock_data_list.append(sale_stock_data)
            all_product_ids.remove(product_id)

        for product_id in all_product_ids:
            sale_stock_data = self._init_collected_data_instance()
            sale_stock_data.product = ProductProduct.browse(product_id)
            sale_stock_data.number_so_lines = 0
            sale_stock_data.ranking = ranking
            sale_stock_data.from_date = from_date
            sale_stock_data.to_date = to_date
            sale_stock_data_list.append(sale_stock_data)

        return sale_stock_data_list, total

    def _build_ordered_level_cumulative_percentage(self):
        """Return an ordered list of tuple of level, cumulative percentage

        The ordering is based on the level with the higher percentage first
        """
        self.ensure_one()
        levels = self.level_ids.sorted(key=attrgetter("percentage"), reverse=True)
        cum_percentages = []
        previous_percentage = None
        for i, level in enumerate(levels):
            perc = level.percentage + level.percentage_products
            if i == 0:
                percentage_to_append = perc
                cum_percentages.append(percentage_to_append)
            else:
                percentage_to_append = previous_percentage + perc
                cum_percentages.append(percentage_to_append)
            previous_percentage = percentage_to_append

        return list(zip(levels, cum_percentages))

    def _get_existing_level_ids(self):
        self.ensure_one()
        self.env.cr.execute(
            """
            SELECT
                id
            FROM
                abc_classification_product_level
            WHERE
                profile_id = %(profile_id)s
        """,
            {"profile_id": self.id},
        )
        return {r[0] for r in self.env.cr.fetchall()}

    def _purge_obsolete_level_values(self, ids_to_remove):
        if not ids_to_remove:
            return
        self.env.cr.execute(
            """
            DELETE FROM
                abc_classification_product_level
            WHERE
                id in %(ids)s
        """,
            {"ids": tuple(ids_to_remove)},
        )

    def _data_to_vals(self, data, create=False):
        self.ensure_one()
        res = {"computed_level_id": data.computed_level.id}
        if create:
            res.update(
                {
                    "product_id": data.product.id,
                    "profile_id": data.profile.id,
                }
            )
        return res

    def _compute_abc_classification(self):
        to_compute_cost = self.filtered(lambda p: p.profile_type == "product_cost")
        to_compute_sale = self.filtered(lambda p: p.profile_type == "sale_stock")
        remaining = self - to_compute_cost - to_compute_sale
        
        res = None
        if remaining:
            res = super(
                AbcClassificationProfile, remaining
            )._compute_abc_classification()
            
        # Handle product cost classification
        ProductClassification = self.env["abc.classification.product.level"]
        
        for profile in to_compute_cost:
            product_cost_data_list, total_cost = profile._get_data()
            existing_level_ids_to_remove = profile._get_existing_level_ids()
            level_percentage = profile._build_ordered_level_cumulative_percentage()
            if not level_percentage:
                continue
                
            level, percentage = level_percentage.pop(0)
            previous_data = {}
            total_products = len(product_cost_data_list)
            percentage_products = (100.0 / total_products) if total_products else 0.0
            
            for i, product_cost_data in enumerate(product_cost_data_list):
                product_cost_data.total_products = total_products
                product_cost_data.percentage_products = percentage_products
                product_cost_data.cumulated_percentage_products = (
                    product_cost_data.percentage_products
                    if i == 0
                    else (
                        product_cost_data.percentage_products
                        + previous_data.cumulated_percentage_products
                    )
                )
                
                # Compute percentages based on product cost
                product_cost_data.percentage = (
                    (100.0 * product_cost_data.product_cost / total_cost) 
                    if total_cost > 0 else 0.0
                )

                product_cost_data.cumulated_percentage = (
                    product_cost_data.percentage
                    if i == 0
                    else (
                        product_cost_data.percentage + previous_data.cumulated_percentage
                    )
                )
                
                if float_round(product_cost_data.cumulated_percentage, 0) > 100:
                    raise UserError(_("Cumulative percentage greater than 100."))

                product_cost_data.sum_cumulated_percentages = (
                    product_cost_data.cumulated_percentage
                    + product_cost_data.cumulated_percentage_products
                )

                # Compute ABC classification
                if (
                    product_cost_data.sum_cumulated_percentages > percentage
                    and len(level_percentage) > 0
                ):
                    level, percentage = level_percentage.pop(0)

                product = product_cost_data.product
                levels = product.abc_classification_product_level_ids
                product_abc_classification = levels.filtered(
                    lambda p, prof=profile: p.profile_id == prof
                )

                product_cost_data.computed_level = level
                if product_abc_classification:
                    existing_level_ids_to_remove.remove(product_abc_classification.id)
                    if product_abc_classification.level_id != level:
                        vals = profile._data_to_vals(
                            product_cost_data, create=False
                        )
                        product_abc_classification.write(vals)
                else:
                    vals = profile._data_to_vals(
                        product_cost_data, create=True
                    )
                    product_abc_classification = ProductClassification.create(vals)
                    
                product_cost_data.total_cost = total_cost
                product_cost_data.product_level = product_abc_classification
                previous_data = product_cost_data
                
            if product_cost_data_list:
                self._log_history(product_cost_data_list)
            profile._purge_obsolete_level_values(existing_level_ids_to_remove)
        
        # Handle sale stock classification (original code)
        for profile in to_compute_sale:
            sale_stock_data_list, total = profile._get_data()
            existing_level_ids_to_remove = profile._get_existing_level_ids()
            level_percentage = profile._build_ordered_level_cumulative_percentage()
            if not level_percentage:
                continue
            level, percentage = level_percentage.pop(0)
            previous_data = {}
            total_products = len(sale_stock_data_list)
            percentage_products = (100.0 / total_products) if total_products else 0.0
            for i, sale_stock_data in enumerate(sale_stock_data_list):
                sale_stock_data.total_products = total_products
                sale_stock_data.percentage_products = percentage_products
                sale_stock_data.cumulated_percentage_products = (
                    sale_stock_data.percentage_products
                    if i == 0
                    else (
                        sale_stock_data.percentage_products
                        + previous_data.cumulated_percentage_products
                    )
                )
                sale_stock_data.percentage = (
                    (100.0 * sale_stock_data.number_so_lines / total) if total else 0.0
                )

                sale_stock_data.cumulated_percentage = (
                    sale_stock_data.percentage
                    if i == 0
                    else (
                        sale_stock_data.percentage + previous_data.cumulated_percentage
                    )
                )
                if float_round(sale_stock_data.cumulated_percentage, 0) > 100:
                    raise UserError(_("Cumulative percentage greater than 100."))

                sale_stock_data.sum_cumulated_percentages = (
                    sale_stock_data.cumulated_percentage
                    + sale_stock_data.cumulated_percentage_products
                )

                if (
                    sale_stock_data.sum_cumulated_percentages > percentage
                    and len(level_percentage) > 0
                ):
                    level, percentage = level_percentage.pop(0)

                product = sale_stock_data.product
                levels = product.abc_classification_product_level_ids
                product_abc_classification = levels.filtered(
                    lambda p, prof=profile: p.profile_id == prof
                )

                sale_stock_data.computed_level = level
                if product_abc_classification:
                    existing_level_ids_to_remove.remove(product_abc_classification.id)
                    if product_abc_classification.level_id != level:
                        vals = profile._data_to_vals(
                            sale_stock_data, create=False
                        )
                        product_abc_classification.write(vals)
                else:
                    vals = profile._data_to_vals(
                        sale_stock_data, create=True
                    )
                    product_abc_classification = ProductClassification.create(vals)
                sale_stock_data.total_so_lines = total
                sale_stock_data.product_level = product_abc_classification
                previous_data = sale_stock_data
            if sale_stock_data_list:
                self._log_history(sale_stock_data_list)
            profile._purge_obsolete_level_values(existing_level_ids_to_remove)
        return res

    def _log_history(self, data_list):
        """Log collected and computed values into history table"""
        if not data_list:
            return
            
        # Validate we have consistent data types
        data_class = type(data_list[0])
        if not all(isinstance(d, data_class) for d in data_list):
            raise ValueError("All data items must be of the same type")
            
        vals = StringIO()
        writer = csv.writer(vals, delimiter=";")
        for data in data_list:
            writer.writerow(data._to_csv_line())
        vals.seek(0)
        
        table = self.env["abc.sale_stock.level.history"]._table
        columns = data_list[0]._get_col_names()
        
        self.env.cr.copy_from(vals, table, columns=columns, sep=";")
        self.env["abc.classification.product.level"].invalidate_cache(
            ["sale_stock_level_history_ids"]
        )


class SaleStockData(object):
    """Sale stock collected data"""
    __slots__ = [
        "product",
        "profile",
        "computed_level",
        "ranking",
        "percentage",
        "cumulated_percentage",
        "number_so_lines",
        "total_so_lines",
        "product_level",
        "from_date",
        "to_date",
        "total_products",
        "percentage_products",
        "cumulated_percentage_products",
        "sum_cumulated_percentages",
    ]

    def _to_csv_line(self):
        """Return values to write into a csv file"""
        return [
            self.product.id,
            self.product.product_tmpl_id.id,
            self.profile.id,
            self.computed_level.id,
            self.profile.warehouse_id.id,
            self.ranking,
            self.percentage,
            self.cumulated_percentage,
            self.number_so_lines,
            self.total_so_lines,
            self.product_level.id,
            self.from_date,
            self.to_date,
            self.total_products,
            self.percentage_products,
            self.cumulated_percentage_products,
            self.sum_cumulated_percentages,
        ]

    @classmethod
    def _get_col_names(cls):
        """Return the ordered list of column names"""
        return [
            "product_id",
            "product_tmpl_id",
            "profile_id",
            "computed_level_id",
            "warehouse_id",
            "ranking",
            "percentage",
            "cumulated_percentage",
            "number_so_lines",
            "total_so_lines",
            "product_level_id",
            "from_date",
            "to_date",
            "total_products",
            "percentage_products",
            "cumulated_percentage_products",
            "sum_cumulated_percentages",
        ]


class ProductCostData(object):
    """Product cost collected data"""
    __slots__ = [
        "product",
        "profile",
        "computed_level",
        "ranking",
        "percentage",
        "cumulated_percentage",
        "product_cost",
        "total_cost",
        "product_level",
        "from_date",
        "to_date",
        "total_products",
        "percentage_products",
        "cumulated_percentage_products",
        "sum_cumulated_percentages",
    ]

    def _to_csv_line(self):
        """Return values to write into a csv file"""
        return [
            self.product.id,
            self.product.product_tmpl_id.id,
            self.profile.id,
            self.computed_level.id,
            self.profile.warehouse_id.id if self.profile.warehouse_id else None,
            self.ranking,
            self.percentage,
            self.cumulated_percentage,
            self.product_cost,
            self.total_cost,
            self.product_level.id,
            self.from_date,
            self.to_date,
            self.total_products,
            self.percentage_products,
            self.cumulated_percentage_products,
            self.sum_cumulated_percentages,
        ]

    @classmethod
    def _get_col_names(cls):
        """Return the ordered list of column names"""
        return [
            "product_id",
            "product_tmpl_id",
            "profile_id",
            "computed_level_id",
            "warehouse_id",
            "ranking",
            "percentage",
            "cumulated_percentage",
            "product_cost",
            "total_cost",
            "product_level_id",
            "from_date",
            "to_date",
            "total_products",
            "percentage_products",
            "cumulated_percentage_products",
            "sum_cumulated_percentages",
        ]