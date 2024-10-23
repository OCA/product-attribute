# Copyright 2020 ForgeFlow S.L.
# Copyright 2024 Tecnativa - Carolina Fernandez
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
        default=lambda self: self.env.company.lot_sequence_padding,
        help="The lots' sequence will be created using this number of digits.",
    )
    lot_sequence_number_next = fields.Integer(
        string="Next Number",
        help="The next sequence number will be used for the next lot.",
        compute="_compute_lot_seq_number_next",
        inverse="_inverse_lot_seq_number_next",
    )
    display_lot_sequence_fields = fields.Boolean(
        compute="_compute_display_lot_sequence_fields"
    )

    @api.depends("tracking")  # For products being created (before saved).
    def _compute_display_lot_sequence_fields(self):
        self.display_lot_sequence_fields = (
            self.env["stock.lot"]._get_sequence_policy() == "product"
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
        seq_policy = self.env["stock.lot"]._get_sequence_policy()
        if seq_policy == "global":
            return super().write(vals)
        else:
            serial_templates = (
                self.filtered(lambda pdt: pdt.tracking in ["lot", "serial"])
                if (
                    not vals.get("tracking", False)
                    or vals.get("tracking", False) == "none"
                )
                else self
            )
            super(ProductTemplate, self - serial_templates).write(vals)
            # templates with sequence
            serial_tmpl_seq = serial_templates.filtered("lot_sequence_id")
            serial_tmpl_wo_seq = serial_templates - serial_tmpl_seq
            new_sequence = self.env["ir.sequence"]
            if len(serial_tmpl_wo_seq) and not vals.get("lot_sequence_id", False):
                new_sequence = serial_tmpl_wo_seq[0].sudo()._create_lot_sequence(vals)
            elif vals.get("lot_sequence_id", False):
                new_sequence = self.env["ir.sequence"].browse(vals["lot_sequence_id"])
            # template with sequence and update it
            for template in serial_tmpl_seq:
                tracking = vals.get("tracking", False) or template.tracking
                if tracking in ["lot", "serial"]:
                    if vals.get("lot_sequence_id", False):
                        lot_sequence_id = self.env["ir.sequence"].browse(
                            vals["lot_sequence_id"]
                        )
                        vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                        vals["lot_sequence_padding"] = lot_sequence_id.padding
            super(ProductTemplate, serial_tmpl_seq).write(vals)
            # template without sequence, set new sequence, prefix and padding
            for template in serial_tmpl_wo_seq:
                tracking = vals.get("tracking", False) or template.tracking
                if tracking in ["lot", "serial"] or vals.get("lot_sequence_id", False):
                    if new_sequence:
                        vals["lot_sequence_id"] = new_sequence.id
                        vals["lot_sequence_prefix"] = new_sequence.prefix
                        vals["lot_sequence_padding"] = new_sequence.padding
            return super(ProductTemplate, serial_tmpl_wo_seq).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        seq_policy = self.env["stock.lot"]._get_sequence_policy()
        for vals in vals_list:
            if seq_policy == "product" and vals.get("tracking", False) in [
                "lot",
                "serial",
            ]:
                if not vals.get("lot_sequence_id", False):
                    vals["lot_sequence_id"] = self.sudo()._create_lot_sequence(vals).id
                else:
                    lot_sequence_id = self.env["ir.sequence"].browse(
                        vals["lot_sequence_id"]
                    )
                    vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                    vals["lot_sequence_padding"] = lot_sequence_id.padding
        return super().create(vals_list)
