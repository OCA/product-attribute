from odoo import api, fields, models

class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    value_group_id = fields.Many2one(
        'product.attribute.value.group',
        string="Value Group",
        domain="[('attribute_id', '=', attribute_id)]",
        help="Select a predefined group of values. This will overwrite the current values."
    )


    @api.onchange('attribute_id')
    def _onchange_attribute_id_clear_group(self):
        if self.attribute_id and self.value_group_id and self.value_group_id.attribute_id != self.attribute_id:
            self.value_group_id = False

    @api.onchange('value_group_id')
    def _onchange_value_group_id(self):
        if self.value_group_id:
            # self.value_ids = [(6, 0, self.value_group_id.value_ids.ids)]
            self.value_ids = self.value_group_id.value_ids
        # else:
            # self.value_ids = [(5, 0, 0)]

    @api.onchange('value_ids')
    def _onchange_value_ids_check_group(self):
        if self.value_group_id:
            group_value_ids = set(self.value_group_id.value_ids.ids)
            current_value_ids = set(self.value_ids.ids)
            if group_value_ids != current_value_ids:
                if self.value_group_id:
                    self.value_group_id = False
