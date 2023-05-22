# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
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

    @api.multi
    def write(self, vals):
        prefix = vals.get("code_prefix")
        for rec in self:
            if vals.get("parent_id"):
                categories = self.env["product.category"].search(
                    [("id", "=", vals["parent_id"])], limit=1
                )
                if categories:
                    if categories.parent_id.sequence_id:
                        if categories.sequence_id != rec.sequence_id:
                            sequence = categories.parent_id.sequence_id
                            vals["code_prefix"] = sequence.prefix
                            vals["sequence_id"] = sequence.id
                    else:
                        vals["code_prefix"] = categories.sequence_id.prefix
                        vals["sequence_id"] = categories.sequence_id.id
            elif rec.parent_id:
                vals["code_prefix"] = rec.parent_id.sequence_id.prefix
                vals["sequence_id"] = rec.parent_id.sequence_id.id
            else:
                if prefix is False:
                    vals["sequence_id"] = ""
                elif prefix:
                    seq_vals = self._prepare_ir_sequence(prefix)
                    vals_sequence = self.env["ir.sequence"].search(
                        [("code", "=", seq_vals["code"])]
                    )
                    if bool(vals_sequence) is False:
                        rec.sequence_id = self.env["ir.sequence"].create(seq_vals)
                    else:
                        rec.sequence_id = vals_sequence
                    childs = self.env["product.category"].search(
                        [("id", "child_of", rec.id)]
                    )
                    for child in childs:
                        child.sequence_id = rec.sequence_id
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix")
        if vals.get("parent_id"):
            categories = self.env["product.category"].search(
                [("id", "=", vals["parent_id"])], limit=1
            )
            for category in categories:
                if category.parent_id.sequence_id:
                    sequence = category.parent_id.sequence_id
                    vals["code_prefix"] = sequence.prefix
                    vals["sequence_id"] = sequence.id
                else:
                    vals["code_prefix"] = categories.sequence_id.prefix
                    vals["sequence_id"] = categories.sequence_id.id
        else:
            if prefix:
                seq_vals = self._prepare_ir_sequence(prefix)
                vals_sequence = self.env["ir.sequence"].search(
                    [("code", "=", seq_vals["code"])]
                )
                if bool(vals_sequence) is False:
                    sequence = self.env["ir.sequence"].create(seq_vals)
                else:
                    sequence = vals_sequence
                vals["sequence_id"] = sequence.id
        return super().create(vals)
