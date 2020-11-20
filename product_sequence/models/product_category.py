# Copyright 2018 ForgeFlow S.L.
#   (http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
        readonly=True,
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

    def write(self, vals):
        prefix = vals.get("code_prefix", False)
        if prefix:
            for rec in self:
                if rec.sequence_id:
                    rec.sudo().sequence_id.prefix = prefix
                else:
                    seq_vals = self._prepare_ir_sequence(prefix)
                    rec.sequence_id = self.env["ir.sequence"].create(seq_vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix", False)
        if prefix:
            seq_vals = self._prepare_ir_sequence(prefix)
            sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().create(vals)
