# Copyright 2025 360ERP (<https://www.360erp.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    average_purchase_price = fields.Float(
        help="Updated periodically according to confirmed purchase orders",
        company_dependent=True,
        readonly=True,
    )

    @api.model
    def update_average_purchase_price(self, templates):
        self = self.sudo()
        templates = templates.sudo()
        companies = self.env["res.company"].search([])
        is_multicompany_env = len(companies.ids) != 1
        if is_multicompany_env:
            shared_tmpl = templates.filtered(lambda tmpl: not tmpl.company_id)
            tmpl = templates - shared_tmpl
            if tmpl:
                self._process_avg_price_multicompany(tmpl)
            if shared_tmpl:
                self._process_avg_price_multicompany_shared(shared_tmpl)
        else:
            self._process_avg_price_monocompany(templates)

    def _process_avg_price_multicompany(self, templates):
        table = self.env["res.currency"]._get_query_currency_table(
            {"multi_company": True, "date": {"date_to": fields.Date.today()}}
        )
        query = """
                SELECT
                    pp.product_tmpl_id,
                    pt.company_id,
                    SUM(
                        (pol.price_unit /
                         (CASE COALESCE(po.currency_rate, 0) WHEN 0 THEN 1.0
                         ELSE po.currency_rate END))
                         *
                        (CASE COALESCE(currency_table.rate, 0) WHEN 0 THEN 1.0
                        ELSE currency_table.rate END)
                    ) / NULLIF(COUNT(pol.id), 0) AS average_price
                FROM purchase_order_line pol
                         JOIN purchase_order po ON pol.order_id = po.id
                         JOIN product_product pp ON pol.product_id = pp.id
                         JOIN product_template pt ON pp.product_tmpl_id = pt.id
                         JOIN {currency_table} ON currency_table.company_id = po.company_id
                WHERE po.state IN ('purchase', 'done')
                  AND pol.product_id IS NOT NULL
                  AND pp.product_tmpl_id IN %s
                GROUP BY pp.product_tmpl_id, pt.company_id;
        """.format(
            currency_table=table
        )
        self.env.cr.execute(query, (tuple(templates.ids),))
        result = self.env.cr.fetchall()
        for product_tmpl_id, cid, avg in result:
            product_template = self.browse(product_tmpl_id)
            if product_template.company_id:
                product_template.with_company(cid).write(
                    {"average_purchase_price": avg}
                )

    def _process_avg_price_multicompany_shared(self, templates):
        table = self.env["res.currency"]._get_query_currency_table(
            {"multi_company": True, "date": {"date_to": fields.Date.today()}}
        )
        query = """
                SELECT
                    pp.product_tmpl_id,
                    SUM(
                        (pol.price_unit /
                         (CASE COALESCE(po.currency_rate, 0) WHEN 0 THEN 1.0
                         ELSE po.currency_rate END))
                         *
                        (CASE COALESCE(currency_table.rate, 0) WHEN 0 THEN 1.0
                        ELSE currency_table.rate END)
                    ) / NULLIF(COUNT(pol.id), 0) AS average_price
                FROM purchase_order_line pol
                         JOIN purchase_order po ON pol.order_id = po.id
                         JOIN product_product pp ON pol.product_id = pp.id
                         JOIN product_template pt ON pp.product_tmpl_id = pt.id
                         JOIN {currency_table} ON currency_table.company_id = po.company_id
                WHERE po.state IN ('purchase', 'done')
                  AND pol.product_id IS NOT NULL
                  AND pp.product_tmpl_id IN %s
                GROUP BY pp.product_tmpl_id;
                """.format(
            currency_table=table
        )
        self.env.cr.execute(query, (tuple(templates.ids),))
        result = self.env.cr.fetchall()
        for el in result:
            product_tmpl_id, avg = el
            for company in self.env["res.company"].search([]):
                self.browse(product_tmpl_id).with_company(company).write(
                    {"average_purchase_price": avg}
                )

    def _process_avg_price_monocompany(self, templates):
        table = self.env["res.currency"]._get_query_currency_table(
            {"multi_company": True, "date": {"date_to": fields.Date.today()}}
        )
        query = """
                SELECT
                    pp.product_tmpl_id,
                    SUM(
                        (pol.price_unit /
                         (CASE COALESCE(po.currency_rate, 0) WHEN 0 THEN 1.0
                         ELSE po.currency_rate END))
                         *
                        (CASE COALESCE(currency_table.rate, 0) WHEN 0 THEN 1.0
                        ELSE currency_table.rate END)
                    ) / NULLIF(COUNT(pol.id), 0) AS average_price
                FROM purchase_order_line pol
                         JOIN purchase_order po ON pol.order_id = po.id
                         JOIN product_product pp ON pol.product_id = pp.id
                         JOIN product_template pt ON pp.product_tmpl_id = pt.id
                         JOIN {currency_table} ON currency_table.company_id = po.company_id
                WHERE po.state IN ('purchase', 'done')
                  AND pol.product_id IS NOT NULL
                  AND pp.product_tmpl_id IN %s
                GROUP BY pp.product_tmpl_id;
                """.format(
            currency_table=table
        )
        self.env.cr.execute(query, (tuple(templates.ids),))
        result = self.env.cr.fetchall()
        for el in result:
            product_tmpl_id, avg = el
            self.browse(product_tmpl_id).write({"average_purchase_price": avg})
