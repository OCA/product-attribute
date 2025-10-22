# Copyright 2020 ForgeFlow S.L.
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    use_specific_lot_sequence = fields.Boolean(
        help="Use an specific lot sequence for this product",
        default=True,
    )
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

    @api.depends("tracking", "use_specific_lot_sequence")
    def _compute_display_lot_sequence_fields(self):
        product_sequence_policy = (
            self.env["stock.lot"]._get_sequence_policy() == "product"
        )
        for product in self:
            product.display_lot_sequence_fields = (
                product_sequence_policy and product.use_specific_lot_sequence
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

    def create_lot_sequence(self):
        self.ensure_one()
        if self.lot_sequence_id:
            return
        self.lot_sequence_id = self._create_lot_sequence({})

    def remove_lot_sequence(self):
        self.ensure_one()
        if not self.lot_sequence_id:
            return
        self.lot_sequence_id.unlink()

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
        # We want to remove the sequence when the user decides that the product won't
        # use it.
        add_lot_sequence = vals.get("use_specific_lot_sequence")
        if seq_policy == "product":
            for template in self:
                if not template.use_specific_lot_sequence and not add_lot_sequence:
                    continue
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
        res = super().write(vals)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        seq_policy = self.env["stock.lot"]._get_sequence_policy()
        for vals in vals_list:
            if seq_policy == "product" and vals.get("tracking", False) in [
                "lot",
                "serial",
            ]:
                if (
                    "use_specific_lot_sequence" in vals
                    and not vals["use_specific_lot_sequence"]
                ):
                    continue
                if not vals.get("lot_sequence_id", False):
                    vals["lot_sequence_id"] = self.sudo()._create_lot_sequence(vals).id
                else:
                    lot_sequence_id = self.env["ir.sequence"].browse(
                        vals["lot_sequence_id"]
                    )
                    vals["lot_sequence_prefix"] = lot_sequence_id.prefix
                    vals["lot_sequence_padding"] = lot_sequence_id.padding
        return super().create(vals_list)
