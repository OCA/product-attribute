# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = ["product.template", "product.mixin.profile"]
    _name = "product.template"

    profile_id = fields.Many2one(comodel_name="product.profile", string="Profile")
    profile_explanation = fields.Text(related="profile_id.explanation", readonly=True)

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """fields_view_get comes from Model (not AbstractModel)"""
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        return self._customize_view(res, view_type)


class ProductProduct(models.Model):
    _inherit = ["product.product", "product.mixin.profile"]
    _name = "product.product"

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        view = self.env["ir.ui.view"].browse(view_id)
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        # This is a simplified view for which the customization do not apply
        if view.name == "product.product.view.form.easy":
            return res
        return self._customize_view(res, view_type)
