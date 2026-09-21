from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    base_pricelist_compute_price_id = fields.Many2one(
        "product.pricelist",
        string="Recomputing pricelist",
        help="Pricelist used to calculate the price of all products",
    )

    @api.model
    def _cron_update_product_list_price(self):
        companies = self.search([("base_pricelist_compute_price_id", "!=", False)])
        for company in companies:
            company.base_pricelist_compute_price_id.with_company(
                company
            )._update_product_price_from_pricelist()
        return True
