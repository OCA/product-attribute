# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackagingLevel(models.Model):
    _name = "product.packaging.level"
    _description = "Level management for product.packaging"
    _order = "sequence, code"

    def _default_language(self):
        lang_code = self.env["ir.default"].get("res.partner", "lang")
        def_lang_id = self.env["res.lang"]._lang_get_id(lang_code)
        return def_lang_id or self._active_languages()[0]

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    active = fields.Boolean(default=True)
    is_default = fields.Boolean()
    default_lang_id = fields.Many2one(
        "res.lang",
        string="Default Language",
        default=lambda self: self._default_language(),
        required=True,
    )

    name_policy = fields.Selection(
        selection=[
            ("by_package_level", "Package Level Name"),
            ("by_package_type", "Package Type Name"),
            ("user_defined", "User Defined"),
        ],
        default="by_package_level",
        help=(
            "config to set name of product packaging. Three options:"
            "- The package level name (default)"
            "- The package type name (if groups='stock.group_tracking_lot')"
            "- user defined: free text value defined"
        ),
    )

    @api.constrains("name_policy")
    def _check_packaging_name(self):
        for packaging in self:
            activated_packages = self.env.user.has_group("stock.group_tracking_lot")
            if packaging.name_policy == "by_package_type" and not activated_packages:
                raise ValidationError(
                    _(
                        "Packaging name based on package type is only allowed"
                        " after activating the option Packages in Inventory >"
                        " Configuration > Settings !"
                    )
                )

    @api.constrains("is_default")
    def _check_is_default(self):
        msg = False
        default_count = self.search_count([("is_default", "=", True)])
        if default_count == 0:
            msg = _('There must be one product packaging level set as "Is Default".')
        elif default_count > 1:
            msg = _('Only one product packaging level can be set as "Is Default".')
        if msg:
            raise ValidationError(msg)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.code)))
        return result
