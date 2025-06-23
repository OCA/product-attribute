import logging
from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round

_logger = logging.getLogger(__name__)

class AbcClassificationProfile(models.Model):
    _inherit = "abc.classification.profile"
    _logger = _logger

    profile_type = fields.Selection(
        selection_add=[
            (
                "cost",
                "Based on the Cost of delivered sale order line by product",
            ),
            (
                "sale_price",
                "Based on the Sale Price of delivered sale order line by product",
            ),
            (
                "sale_margin",
                "Based on the Sale Margin of delivered sale order line by product",
            ),
        ],
        ondelete={"cost": "cascade", "sale_price": "cascade", "sale_margin": "cascade"},
    )

    @api.constrains("profile_type", "warehouse_id")
    def _check_warehouse_id(self):
        for rec in self:
            if (
                rec.profile_type in ["sale_stock", "cost", "sale_price", "sale_margin"]
                and not rec.warehouse_id
            ):
                raise ValidationError(
                    _("You must specify a warehouse for {profile_name}").format(
                        profile_name=rec.name
                    )
                )
    
    @api.model
    def _finance_get_collected_data_class(self):
        return FinanceSaleData
    
    def _finance_init_collected_data_instance(self):
        self.ensure_one()
        finance_sale_data = self._finance_get_collected_data_class()()
        finance_sale_data.profile = self
        return finance_sale_data

    def _get_finance_data_query(self, from_date, customer_location_ids):
        """
        Build a query to aggregate financial data by product for ABC classification, depending on profile_type.
        - cost: SUM(sol.purchase_price * sol.qty_delivered) as total_cost
        - sale_price: SUM(sol.price_unit * sol.qty_delivered) as total_sales
        - margin: SUM(sol.margin) as total_margin (already line-level total)
        """
        if self.profile_type == "cost":
            select_col = "SUM(sol.purchase_price * sol.qty_delivered) AS total_cost"
            order_col = "total_cost"
        elif self.profile_type == "sale_price":
            select_col = "SUM(sol.price_unit * sol.qty_delivered) AS total_sales"
            order_col = "total_sales"
        elif self.profile_type == "sale_margin":
            select_col = "SUM(sol.margin) AS total_margin"
            order_col = "total_margin"

        query = f"""
            SELECT
                sol.product_id AS product_id,
                {select_col}
            FROM
                sale_order so
            JOIN
                sale_order_line sol ON sol.order_id = so.id
            JOIN
                abc_classification_profile_product_rel rel ON rel.product_id = sol.product_id
            JOIN
                product_product pp ON pp.id = sol.product_id
            WHERE
                sol.qty_delivered > 0
                AND pp.active
                AND rel.profile_id = %(profile_id)s
                AND so.warehouse_id = %(current_warehouse_id)s
                AND EXISTS (
                    SELECT 1 FROM stock_move sm
                    WHERE sm.date > %(start_date)s
                        AND sm.location_dest_id in %(customer_loc_ids)s
                        AND sm.sale_line_id = sol.id
                )
            GROUP BY sol.product_id
            ORDER BY {order_col} DESC
        """
        params = {
            "start_date": from_date,
            "current_warehouse_id": self.warehouse_id.id,
            "profile_id": self.id,
            "customer_loc_ids": tuple(customer_location_ids),
        }
        return query, params

    def _finance_get_data(self, from_date=None):
        """Get a list of statics info from the DB ordered by number of lines desc"""
        self.ensure_one()
        if self.profile_type not in ("cost", "sale_price", "sale_margin"):
            raise UserError(_("Profile type must be cost, sale_price or sale_margin"))
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
        query, params = self._get_finance_data_query(
            from_date, customer_location_ids
        )
        self.env.cr.execute(query, params)
        result = self.env.cr.fetchall()
        total = 0
        finance_data_list = []
        ranking = 1
        ProductProduct = self.env["product.product"]
        # Map SQL result into FinanceSaleData fields
        for r in result:
            finance_data = self._finance_init_collected_data_instance()
            product_id = r[0]
            finance_data.product = ProductProduct.browse(product_id)
            # Map aggregate value to the right field
            exclude_from_abc = False
            if self.profile_type == "cost":
                finance_data.total_cost = float(r[1] or 0.0)
                finance_data.total_sales = 0.0
                finance_data.margin = 0.0
            elif self.profile_type == "sale_price":
                finance_data.total_cost = 0.0
                finance_data.total_sales = float(r[1] or 0.0)
                finance_data.margin = 0.0
            elif self.profile_type == "sale_margin":
                margin_val = float(r[1] or 0.0)
                finance_data.total_cost = 0.0
                finance_data.total_sales = 0.0
                finance_data.margin = margin_val
                if margin_val < 0:
                    exclude_from_abc = True
            # Always set purchase_price (standard cost) from product.template
            tmpl = finance_data.product.product_tmpl_id
            finance_data.purchase_price = float(
                getattr(tmpl, 'standard_price', 0.0) or 0.0
            )
            finance_data.ranking = ranking
            finance_data.from_date = from_date
            finance_data.to_date = to_date
            if not exclude_from_abc:
                ranking += 1
                total += float(r[1] or 0.0)
                finance_data_list.append(finance_data)
            all_product_ids.remove(product_id)

        # Optionally, handle negative-margin products separately here (e.g., assign to a special class or report them)
        # Add all products not sold or not delivered into this timelapse
        for product_id in all_product_ids:
            finance_data = self._finance_init_collected_data_instance()
            finance_data.product = ProductProduct.browse(product_id)
            finance_data.purchase_price = float(
                getattr(finance_data.product.product_tmpl_id, 'standard_price', 0.0) or 0.0
            )
            finance_data.total_cost = 0.0
            finance_data.total_sales = 0.0
            finance_data.margin = 0.0
            finance_data.ranking = ranking
            finance_data.from_date = from_date
            finance_data.to_date = to_date
            finance_data_list.append(finance_data)

        return finance_data_list, total

    def _finance_data_to_vals(self, finance_data, create=False):
        self.ensure_one()
        res = {"computed_level_id": finance_data.computed_level.id}
        if create:
            res.update(
                {
                    "product_id": finance_data.product.id,
                    "profile_id": finance_data.profile.id,
                }
            )
        return res

    def _compute_abc_classification(self):
        # Only process finance profile types in this module
        finance_types = ("cost", "sale_price", "sale_margin")
        to_compute = self.filtered(lambda p: p.profile_type in finance_types)
        remaining = self - to_compute
        res = None
        if remaining:
            # Delegate to super for non-finance profiles
            res = super()._compute_abc_classification()
        ProductClassification = self.env["abc.classification.product.level"]

        for profile in to_compute:
            # Get finance data per product (list of FinanceSaleData), plus total for percentage computation
            finance_data_list, total_value = profile._finance_get_data()
            existing_level_ids_to_remove = profile._get_existing_level_ids()
            level_percentage = profile._build_ordered_level_cumulative_percentage()
            if not level_percentage:
                continue
            level, percentage = level_percentage.pop(0)
            previous_data = None
            total_products = len(finance_data_list)
            percentage_products = (100.0 / total_products) if total_products else 0.0
            # Pick the correct value field for this profile type
            if profile.profile_type == "cost":
                value_field = "total_cost"
            elif profile.profile_type == "sale_price":
                value_field = "total_sales"
            elif profile.profile_type == "sale_margin":
                value_field = "margin"
            else:
                raise UserError(
                    _(f"Unknown finance profile_type: {profile.profile_type}")
                )

            for i, finance_data in enumerate(finance_data_list):
                finance_data.total_products = total_products
                finance_data.percentage_products = percentage_products
                finance_data.cumulated_percentage_products = (
                    finance_data.percentage_products
                    if i == 0
                    else (
                        finance_data.percentage_products
                        + previous_data.cumulated_percentage_products
                    )
                )
                # Compute percentages and cumulative percentages for the products
                value = getattr(finance_data, value_field, 0.0) or 0.0
                finance_data.percentage = (
                    (100.0 * value / total_value) if total_value else 0.0
                )
                finance_data.cumulated_percentage = (
                    finance_data.percentage
                    if i == 0
                    else (finance_data.percentage + previous_data.cumulated_percentage)
                )
                # Debug logging for cumulative percentage
                _logger.info(
                    "[ABC] Product %s: value=%.4f, total_value=%.4f, percentage=%.4f, cumulated_percentage=%.4f",
                    finance_data.product.display_name,
                    value,
                    total_value,
                    finance_data.percentage,
                    finance_data.cumulated_percentage,
                )
                # Allow for floating point imprecision: round to 2 decimals and allow up to 101
                if float_round(finance_data.cumulated_percentage, 2) > 100.01:
                    _logger.info(
                        "[ABC] ERROR: Product %s cumulative percentage exceeded: %.4f (value=%.4f, total_value=%.4f)",
                        finance_data.product.display_name,
                        finance_data.cumulated_percentage,
                        value,
                        total_value,
                    )
                    raise UserError(_("Cumulative percentage greater than 100 (actual: %.4f)." 
                    % finance_data.cumulated_percentage)
                )
                finance_data.sum_cumulated_percentages = (
                    finance_data.cumulated_percentage
                    + finance_data.cumulated_percentage_products
                )
                # Compute ABC classification for the products based on the
                # sum of cumulated percentages
                if (
                    finance_data.sum_cumulated_percentages > percentage
                    and len(level_percentage) > 0
                ):
                    level, percentage = level_percentage.pop(0)
                product = finance_data.product
                levels = product.abc_classification_product_level_ids
                product_abc_classification = levels.filtered(
                    lambda p, prof=profile: p.profile_id == prof
                )
                finance_data.computed_level = level
                if product_abc_classification:
                    # The line is still significant...
                    existing_level_ids_to_remove.remove(product_abc_classification.id)
                    if product_abc_classification.level_id != level:
                        vals = profile._finance_data_to_vals(finance_data, create=False)
                        product_abc_classification.write(vals)
                else:
                    vals = profile._finance_data_to_vals(finance_data, create=True)
                    product_abc_classification = ProductClassification.create(vals)
                finance_data.product_level = product_abc_classification
                previous_data = finance_data
            if finance_data_list:
                profile._finance_log_history(finance_data_list)
            profile._purge_obsolete_level_values(existing_level_ids_to_remove)
        return res

    def _finance_log_history(self, finance_data_list):
        """Log the financial ABC classification history for this profile."""
        import csv
        import io
        cr = self.env.cr
        table = "abc_finance_sale_level_history"
        columns = FinanceSaleData._get_col_names()
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=";", lineterminator="\n")
        for finance_data in finance_data_list:
            writer.writerow(finance_data._to_csv_line())
        buf.seek(0)
        cr.copy_from(buf, table, columns=columns, sep=";")
        # Ensure ORM sees the new records for tests
        self.env['abc.finance.sale.level.history'].flush()

class FinanceSaleData(object):
    """Finance ABC classification data

    This class is used to store all the collected and computed financial data for
    ABC classification at the product level. It provides methods for bulk
    inserting data into the abc.finance.sale.level.history table.
    """

    __slots__ = [
        "product",
        "profile",
        "computed_level",
        "ranking",
        "percentage",
        "cumulated_percentage",
        "purchase_price",
        "total_cost",
        "total_sales",
        "margin",
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
            self.computed_level.id if self.computed_level else None,
            self.profile.warehouse_id.id if self.profile.warehouse_id else None,
            self.ranking or 0,
            self.percentage or 0.0,
            self.cumulated_percentage or 0.0,
            float(self.purchase_price or 0.0),
            float(self.total_cost or 0.0),
            float(self.total_sales or 0.0),
            float(self.margin or 0.0),
            self.product_level.id if self.product_level else None,
            self.from_date or fields.Date.today(),
            self.to_date or fields.Date.today(),
            self.total_products or 0,
            self.percentage_products or 0.0,
            self.cumulated_percentage_products or 0.0,
            self.sum_cumulated_percentages or 0.0,
        ]

    @classmethod
    def _get_col_names(cls):
        """Return the ordered list of column names for the financial ABC history table"""
        return [
            "product_id",
            "product_tmpl_id",
            "profile_id",
            "computed_level_id",
            "warehouse_id",
            "ranking",
            "percentage",
            "cumulated_percentage",
            "purchase_price",
            "total_cost",
            "total_sales",
            "margin",
            "product_level_id",
            "from_date",
            "to_date",
            "total_products",
            "percentage_products",
            "cumulated_percentage_products",
            "sum_cumulated_percentages",
        ]