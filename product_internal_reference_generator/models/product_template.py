# Copyright 2023 Ooops - Ilyas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    int_ref_template_id = fields.Many2one(
        "product.code.sequence", "Internal Reference Template", copy=True
    )
    variants_sequence_id = fields.Many2one("ir.sequence", copy=False)
    variants_prefix = fields.Char(
        "Internal Reference Prefix", readonly=True, tracking=True, copy=False
    )
    default_code = fields.Char(copy=False)

    @api.onchange("int_ref_template_id")
    def onchange_int_ref_template_id(self):
        self.variants_prefix = False

    def btn_generate_sequence(self):
        self.ensure_one()
        int_ref_next_val = self.int_ref_template_id.sequence_id.next_by_id()
        var_seq = (
            self.env["ir.sequence"]
            .sudo()
            .create(
                {
                    "name": "variants " + int_ref_next_val,
                    "padding": self.int_ref_template_id.variant_reference_numbers,
                }
            )
        )
        self.write(
            {
                "variants_prefix": int_ref_next_val,
                "variants_sequence_id": var_seq.id,
                "default_code": int_ref_next_val + var_seq.get_next_char(0),
            }
        )
        self.update_variants_default_code()

    def update_variants_default_code(self):
        for pp in self.product_variant_ids.filtered(lambda p: not p.default_code):
            pp.default_code = self.get_variant_next_default_code()

    def get_variant_next_default_code(self):
        if self.variants_sequence_id:
            return self.variants_prefix + self.variants_sequence_id.next_by_id()
        return False
