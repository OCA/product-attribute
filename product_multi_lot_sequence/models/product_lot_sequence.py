# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductLotSequence(models.Model):
    _name = "product.lot.sequence"
    _description = "Product Lot Sequence"

    name = fields.Char(default="/")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Assigns the priority to the list of product lot sequences.",
    )
    product_id = fields.Many2one("product.product", string="Product Variant")
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product Template",
        index=True,
        ondelete="cascade",
        domain="[('tracking', 'in', ['lot', 'serial'])]",
    )

    lot_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Entry Sequence",
        help="This field contains the information related to the " "numbering of lots.",
        copy=False,
    )
    lot_sequence_prefix = fields.Char(
        string="Sequence Prefix",
        help="The lot's sequence will be created using this prefix.",
    )
    lot_sequence_suffix = fields.Char(
        string="Sequence Suffix",
        help="The lot's sequence will be created using this suffix.",
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
        """ Create new no_gap entry sequence"""
        name = vals.get("name", False) or self.name
        prefix = vals.get("lot_sequence_prefix", False) or self.lot_sequence_prefix
        padding = vals.get("lot_sequence_padding") or self.lot_sequence_padding
        suffix = vals.get("lot_sequence_suffix") or self.lot_sequence_suffix
        seq = {
            "name": name,
            "implementation": "no_gap",
            "prefix": prefix,
            "padding": padding,
            "suffix": suffix,
            "number_increment": 1,
            "use_date_range": False,
        }
        seq = self.env["ir.sequence"].create(seq)
        seq_date_range = seq._get_current_sequence()
        seq_date_range.number_next = self.lot_sequence_number_next or vals.get(
            "lot_sequence_number_next", 1
        )
        return seq

    @api.multi
    # do not depend on 'lot_sequence_id.date_range_ids', because
    # lot_sequence_id._get_current_sequence() may invalidate it!
    @api.depends("lot_sequence_id.use_date_range", "lot_sequence_id.number_next_actual")
    def _compute_lot_seq_number_next(self):
        """Compute 'lot_sequence_number_next' according to the current
        sequence in use, an ir.sequence or an ir.sequence.date_range.
        """
        for p_sequence in self:
            if p_sequence.lot_sequence_id:
                sequence = p_sequence.lot_sequence_id._get_current_sequence()
                p_sequence.lot_sequence_number_next = sequence.number_next_actual
            else:
                p_sequence.lot_sequence_number_next = 1

    @api.multi
    def _inverse_lot_seq_number_next(self):
        """
        Inverse 'lot_sequence_number_next' to edit the current sequence next
        number
        """
        for p_sequence in self:
            if p_sequence.lot_sequence_id and p_sequence.lot_sequence_number_next:
                sequence = p_sequence.lot_sequence_id._get_current_sequence()
                sequence.sudo().number_next = p_sequence.lot_sequence_number_next

    @api.multi
    def write(self, vals):
        for p_sequence in self:
            tracking = p_sequence.product_tmpl_id.tracking
            if tracking in ["lot", "serial"]:
                if not vals.get("lot_sequence_id", False):
                    vals["lot_sequence_id"] = (
                        p_sequence.sudo()._create_lot_sequence(vals).id
                    )
                else:
                    lot_sequence_id = self.env["ir.sequence"].browse(
                        vals["lot_sequence_id"]
                    )
                    vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                    vals["lot_sequence_suffix"] = lot_sequence_id.suffix
                    vals["lot_sequence_padding"] = lot_sequence_id.padding

        return super().write(vals)

    @api.model
    def create(self, vals):
        if not vals.get("lot_sequence_id", False):
            vals["lot_sequence_id"] = self.sudo()._create_lot_sequence(vals).id
        else:
            lot_sequence_id = self.env["ir.sequence"].browse(vals["lot_sequence_id"])
            vals["lot_sequence_prefix"] = lot_sequence_id.prefix
            vals["lot_sequence_suffix"] = lot_sequence_id.suffix
            vals["lot_sequence_padding"] = lot_sequence_id.padding
        return super().create(vals)
