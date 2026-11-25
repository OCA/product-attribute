# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    sequence = fields.Integer(
        compute="_compute_sequence",
        store=True,
        readonly=False,
    )
    display_sequence = fields.Integer(related="sequence", string="Seq.")

    @api.model
    def _get_sequence_depends(self):
        depends = [
            "attribute_id",
            "attribute_id.sort_alphabetically",
            "attribute_id.keep_manual_sort",
            "attribute_id.sort_field",
            "attribute_id.value_ids",
        ]
        for key, _label in self.env["product.attribute"]._selection_sort_field():
            depends.append(f"attribute_id.value_ids.{key}")
        return depends

    @api.model
    def _get_alphabetical_sort_key(self, value, sort_field):
        field_value = value[sort_field]
        if isinstance(field_value, models.BaseModel):
            field_value = field_value.display_name
        return (str(field_value or "").casefold(), value._origin.id or 0)

    @api.depends(lambda self: self._get_sequence_depends())
    def _compute_sequence(self):
        for record in self:
            record.sequence = record.sequence or 0
        for attribute in self.attribute_id:
            if not attribute.is_value_sequence_computed:
                continue
            ordered = attribute.value_ids.sorted(
                key=lambda v, f=attribute.sort_field: self._get_alphabetical_sort_key(
                    v, f
                )
            )
            ranks = {value: index for index, value in enumerate(ordered, start=1)}
            for record in self.filtered(lambda r, a=attribute: r.attribute_id == a):
                if record in ranks:
                    record.sequence = ranks[record]
