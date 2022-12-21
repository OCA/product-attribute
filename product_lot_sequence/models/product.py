# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    lot_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Entry Sequence",
        help="This field contains the information related to the numbering of lots.",
        copy=False,
    )
    lot_sequence_prefix = fields.Char(
        string="Sequence Prefix",
        help="The lot's sequence will be created using this prefix.",
    )
    lot_sequence_padding = fields.Integer(
        string="Sequence Number of Digits",
        default=7,
        help="The lots' sequence will be created using this number of digits.",
    )
    lot_sequence_number_next = fields.Integer(
        string="Next Number",
        help="The next sequence number will be used for the next lot.",
        compute="_compute_lot_seq_number_next",
        inverse="_inverse_lot_seq_number_next",
    )

    @api.model
    def _create_lot_sequence(self, vals):
        """Create new no_gap entry sequence"""
        name = vals.get("name", False) or self.name
        prefix = vals.get("lot_sequence_prefix", False) or self.lot_sequence_prefix
        padding = vals.get("lot_sequence_padding") or self.lot_sequence_padding
        seq = {
            "name": name,
            "implementation": "no_gap",
            "prefix": prefix,
            "padding": padding,
            "number_increment": 1,
            "use_date_range": False,
        }
        seq = self.env["ir.sequence"].create(seq)
        seq_date_range = seq._get_current_sequence()
        seq_date_range.number_next = self.lot_sequence_number_next or vals.get(
            "lot_sequence_number_next", 1
        )
        return seq

    # do not depend on 'lot_sequence_id.date_range_ids', because
    # lot_sequence_id._get_current_sequence() may invalidate it!
    @api.depends("lot_sequence_id.use_date_range", "lot_sequence_id.number_next_actual")
    def _compute_lot_seq_number_next(self):
        """
        Compute 'lot_sequence_number_next' according to the current sequence in use, an
        ir.sequence or an ir.sequence.date_range.
        """
        for template in self:
            if template.lot_sequence_id:
                sequence = template.lot_sequence_id._get_current_sequence()
                template.lot_sequence_number_next = sequence.number_next_actual
            else:
                template.lot_sequence_number_next = 1

    def _inverse_lot_seq_number_next(self):
        """
        Inverse 'lot_sequence_number_next' to edit the current sequence next number
        """
        for template in self:
            if template.lot_sequence_id and template.lot_sequence_number_next:
                sequence = template.lot_sequence_id._get_current_sequence()
                sequence.sudo().number_next = template.lot_sequence_number_next

    def write(self, vals):
        for template in self:
            tracking = vals.get("tracking", False) or template.tracking
            if tracking in ["lot", "serial"]:
                if (
                    not vals.get("lot_sequence_id", False)
                    and not template.lot_sequence_id
                ):
                    vals["lot_sequence_id"] = (
                        template.sudo()._create_lot_sequence(vals).id
                    )
                elif vals.get("lot_sequence_id", False):
                    lot_sequence_id = self.env["ir.sequence"].browse(
                        vals["lot_sequence_id"]
                    )
                    vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                    vals["lot_sequence_padding"] = lot_sequence_id.padding
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get("tracking", False) in ["lot", "serial"]:
            if not vals.get("lot_sequence_id", False):
                vals["lot_sequence_id"] = self.sudo()._create_lot_sequence(vals).id
            else:
                lot_sequence_id = self.env["ir.sequence"].browse(
                    vals["lot_sequence_id"]
                )
                vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                vals["lot_sequence_padding"] = lot_sequence_id.padding
        return super().create(vals)
