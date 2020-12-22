# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = ["product.template", "product.mixin.profile"]
    _name = "product.template"

    profile_id = fields.Many2one(comodel_name="product.profile", string="Profile")
    profile_explanation = fields.Text(related="profile_id.explanation", readonly=True)

    @api.model
    def _fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """ fields_view_get comes from Model (not AbstractModel) """
        res = super()._fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        return self._customize_view(res, view_type)


class ProductProduct(models.Model):
    _inherit = ["product.product", "product.mixin.profile"]
    _name = "product.product"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        view = self.env["ir.ui.view"].browse(view_id)
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        # This is a simplified view for which the customization do not apply
        if view.name == "product.product.view.form.easy":
            return res
        return self._customize_view(res, view_type)
