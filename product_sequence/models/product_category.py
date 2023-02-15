# Copyright 2018 ForgeFlow S.L.
#   (http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = "product.category"

    code_prefix = fields.Char(
        string="Prefix for Product Internal Reference",
        help="Prefix used to generate the internal reference for products "
        "created with this category. If blank the "
        "default sequence will be used.",
    )
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Product Sequence",
        help="This field contains the information related to the numbering "
        "of the journal entries of this journal.",
        copy=False,
    )

    @api.model
    def _prepare_ir_sequence(self, prefix):
        """Prepare the vals for creating the sequence
        :param prefix: a string with the prefix of the sequence.
        :return: a dict with the values.
        """
        vals = {
            "name": "Product " + prefix,
            "code": "product.product - " + prefix,
            "padding": 5,
            "prefix": prefix,
            "company_id": False,
        }
        return vals

    def _get_or_create_sequence(self, prefix):
        seq_vals = self._prepare_ir_sequence(prefix)
        sequence = self.env["ir.sequence"].search(
            [("code", "=", seq_vals.get("code")), ("prefix", "=", prefix)]
        )
        if not sequence:
            sequence = self.env["ir.sequence"].create(seq_vals)
        return sequence

    def write(self, vals):
        sequence_ids_to_check = set()
        if "code_prefix" in vals:
            prefix = vals.get("code_prefix")
            if prefix:
                for rec in self:
                    if rec.sequence_id:
                        sequence_sudo = rec.sudo()
                        sequence_ids_to_check.add(sequence_sudo.id)
                        sequence_sudo.with_context(
                            _no_sequence_prefix_check=True
                        ).sequence_id.prefix = prefix
                    else:
                        vals["sequence_id"] = self._get_or_create_sequence(prefix).id
            else:
                vals["sequence_id"] = False
        res = super().write(vals)
        if sequence_ids_to_check:
            self.env["ir.sequence"].sudo().browse(
                sequence_ids_to_check
            )._check_prefix_product_category()
        return res

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix", False)
        if prefix:
            vals["sequence_id"] = self._get_or_create_sequence(prefix).id
        return super().create(vals)

    @api.constrains("code_prefix", "sequence_id")
    def _check_prefix_sequence_id(self):
        for rec in self:
            if rec.sequence_id and rec.code_prefix != rec.sequence_id.prefix:
                raise ValidationError(
                    _(
                        "The prefix defined on product category %s does not match "
                        "the prefix of linked sequence"
                    )
                    % rec.name
                )
