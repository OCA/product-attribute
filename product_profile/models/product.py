# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _

PROFILE_MENU = _(
    "Sales > Configuration \n> Product Categories and Attributes"
    "\n> Product Profiles"
)
# Prefix name of profile fields setting a default value,
# not an immutable value according to profile
PROF_DEFAULT_STR = "profile_default_"
LEN_DEF_STR = len(PROF_DEFAULT_STR)


def format_except_message(error, field, self):
    value = self.profile_id[field]
    model = type(self)._name
    message = _(
        "Issue\n------\n"
        "%s\n'%s' value can't be applied to '%s' field."
        "\nThere is no matching value between 'Product Profiles' "
        "\nand '%s' models for this field.\n\n"
        "Resolution\n----------\n"
        "Check your settings on Profile model:\n%s"
        % (error, value, field, model, PROFILE_MENU)
    )
    return message


def get_profile_fields_to_exclude():
    # These fields must not be synchronized between product.profile
    # and product.template/product
    return models.MAGIC_COLUMNS + [
        "name",
        "explanation",
        "sequence",
        "display_name",
        "__last_update",
    ]


class ProductTemplate(models.Model):
    _inherit = ["product.template", "product.mixin.profile"]
    _name = "product.template"

    profile_id = fields.Many2one(
        comodel_name="product.profile", string="Profile"
    )
    profile_explanation = fields.Text(
        related="profile_id.explanation", readonly=True
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """ fields_view_get comes from Model (not AbstractModel) """
        res = super(ProductTemplate, self).fields_view_get(
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
        res = super(ProductProduct, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        # This is a simplified view for which the customization do not apply
        if view.name == "product.product.view.form.easy":
            return res
        return self._customize_view(res, view_type)
