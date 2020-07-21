# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from collections import OrderedDict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackagingType(models.Model):
    _name = "product.packaging.type"
    _description = "Type management for product.packaging"
    _order = "sequence, code"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    active = fields.Boolean(default=True)
    is_default = fields.Boolean()

    @api.constrains("is_default")
    def _check_is_default(self):
        msg = False
        default_count = self.search_count([("is_default", "=", True)])
        if default_count == 0:
            msg = _('There must be one product packaging type set as "Is Default".')
        elif default_count > 1:
            msg = _('Only one product packaging type can be set as "Is Default".')
        if msg:
            raise ValidationError(msg)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.code)))
        return result


class ProductPackaging(models.Model):
    _inherit = "product.packaging"
    _order = "product_id, type_sequence"

    def default_packaging_type_id(self):
        return self.env["product.packaging.type"].search(
            [("is_default", "=", True)], limit=1
        )

    packaging_type_id = fields.Many2one(
        "product.packaging.type",
        required=True,
        ondelete="restrict",
        default=lambda p: p.default_packaging_type_id(),
    )
    # Used for the unique constraint
    packaging_type_is_default = fields.Boolean(
        string="Default Packaging Type",
        related="packaging_type_id.is_default",
        store=True,
    )
    type_has_gtin = fields.Boolean(readonly=True, compute="_compute_type_has_gtin")

    type_sequence = fields.Integer(
        string="Type sequence",
        related="packaging_type_id.sequence",
        readonly=True,
        store=True,
    )
    qty_per_type = fields.Html(
        compute="_compute_qty_per_type", string="Qty per package type"
    )

    _sql_constraints = [
        (
            # We *have* to allow several packaging using the default type,
            # because when we install the module on an existing database,
            # the default value will be set to default. Not ideal, but
            # can't do better.
            "product_packaging_type_unique",
            "EXCLUDE (product_id WITH =, packaging_type_id WITH =) "
            "WHERE (packaging_type_is_default is null "
            "OR packaging_type_is_default = false)",
            "It is forbidden to have different packagings "
            "with the same type for a given product.",
        )
    ]

    @api.depends("packaging_type_id", "packaging_type_id.has_gtin", "qty")
    def _compute_type_has_gtin(self):
        for packaging in self:
            packaging.type_has_gtin = packaging.packaging_type_id.has_gtin
            if not packaging.qty:
                packaging.type_has_gtin = False

    @api.depends(
        "product_id",
        "product_id.packaging_ids",
        "packaging_type_id",
        "packaging_type_id.code",
    )
    def _compute_qty_per_type(self):
        for packaging in self:
            product = packaging.product_id
            if not product:
                packaging.qty_per_type = ""
                continue

            smaller_product_packagings = product.packaging_ids.filtered(
                lambda p: p.id != packaging.id and packaging.qty > p.qty > 0.0
            )
            res = OrderedDict()
            for p_pack in smaller_product_packagings.sorted(lambda p: p.qty):
                res[p_pack.packaging_type_id.code] = p_pack.qty
            packaging.qty_per_type = packaging._format_qty_per_type(res)

    def _format_qty_per_type(self, qty_per_type_dict):
        self.ensure_one()
        res = []
        for code, qty in qty_per_type_dict.items():
            new_qty = self.qty / qty
            if not new_qty.is_integer():
                new_qty_int = int(new_qty)
                new_qty_decimals = new_qty - new_qty_int
                new_qty = '{}<span style="color: red;">{}</span>'.format(
                    new_qty_int, str(new_qty_decimals).lstrip("0")
                )
            res.append("{} {}".format(new_qty, code))
        return "; ".join(res)

    @api.onchange("packaging_type_id")
    def _onchange_name(self):
        if self.packaging_type_id:
            self.name = self.packaging_type_id.name

    def name_get(self):
        result = []
        for record in self:
            if record.product_id and record.packaging_type_id:
                result.append((record.id, record.packaging_type_id.display_name))
            else:
                result.append((record.id, record.name))
        return result
