from odoo import api, fields, models


class ProductStickerMixin(models.AbstractModel):
    _name = "product.sticker.mixin"
    _description = "Product Sticker Mixin"

    sticker_ids = fields.One2many(
        comodel_name="product.sticker",
        # `inverse_name` will be needed in every _inherit
        string="Product Stickers",
        domain=lambda s: s.env["product.sticker"]._build_sticker_domain_company(),
    )
    sticker_count = fields.Integer(
        compute="_compute_sticker_count",
        store=True,
    )

    @api.depends("sticker_ids")
    @api.depends_context("company")
    def _compute_sticker_count(self):
        company_domain = self.env["product.sticker"]._build_sticker_domain_company()
        for record in self:
            record.sticker_count = len(
                record.sudo().sticker_ids.filtered_domain(company_domain)
            )
