# Copyright 2026 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = "product.category"

    barcode_prefix = fields.Char(
        help="Prefix used to generate EAN barcodes for products "
        "created with this category. Should be 1-12 digits.",
        compute="_compute_barcode_fields",
        inverse="_inverse_barcode_prefix",
        size=12,
        store=True,
    )
    barcode_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        help="Sequence used to generate unique barcode numbers for products "
        "in this category.",
        compute="_compute_barcode_fields",
        inverse="_inverse_barcode_sequence_prefix",
        store=True,
        copy=False,
    )
    auto_generate_barcode = fields.Boolean(
        help="Automatically generate EAN barcode when creating products "
        "in this category.",
    )

    @api.constrains("barcode_prefix")
    def _check_barcode_prefix(self):
        """Validate barcode prefix contains only digits and correct length."""
        for category in self.filtered("barcode_prefix"):
            if not category.barcode_prefix.isdigit():
                raise UserError(_("Barcode prefix must contain only digits"))
            if len(category.barcode_prefix) > 12:
                raise UserError(_("Barcode prefix cannot exceed 12 digits"))
            if len(category.barcode_prefix) == 0:
                raise UserError(_("Barcode prefix cannot be empty"))

    @api.depends("barcode_sequence_id.prefix")
    def _compute_barcode_fields(self):
        """Compute barcode_prefix from barcode_sequence_id and vice versa."""
        for category in self:
            category.barcode_prefix = category.barcode_sequence_id.prefix

    @api.depends("barcode_prefix")
    def _inverse_barcode_prefix(self):
        """When barcode_prefix is set, find or create corresponding sequence."""
        for category in self:
            if category.barcode_prefix:
                category.barcode_sequence_id = (
                    category._create_or_update_barcode_sequence()
                )

    def _create_or_update_barcode_sequence(self):
        if not self.barcode_prefix:
            return False
        existing_sequence = self.env["ir.sequence"].search(
            [
                ("prefix", "=", self.barcode_prefix),
                ("code", "like", "product.barcode"),
                ("company_id", "=", False),
            ],
            limit=1,
        )
        if existing_sequence:
            return existing_sequence
        else:
            seq_vals = self._prepare_barcode_sequence()
            return self.env["ir.sequence"].create(seq_vals)

    @api.model
    def _prepare_barcode_sequence(self):
        vals = {
            "name": "Barcode " + self.barcode_prefix,
            "code": "product.barcode - " + self.barcode_prefix,
            "padding": 12 - len(self.barcode_prefix),  # Total 13 digits for EAN-13
            "prefix": self.barcode_prefix,
            "company_id": False,
        }
        return vals
