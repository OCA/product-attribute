from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    base_pricelist_compute_price_id = fields.Many2one(
        "product.pricelist",
        related="company_id.base_pricelist_compute_price_id",
        readonly=False,
    )
    main_company_compute_price_id = fields.Many2one(
        "res.company",
        config_parameter="main_company_compute_price_id",
        string="Main company for compute sale price",
        readonly=False,
    )

    def action_update_product_price_from_pricelist(self):
        self.ensure_one()
        pricelist = self.company_id.base_pricelist_compute_price_id
        pricelist._update_product_price_from_pricelist()
