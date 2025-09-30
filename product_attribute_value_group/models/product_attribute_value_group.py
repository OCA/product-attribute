from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductAttributeValueGroup(models.Model):
    _name = "product.attribute.value.group"
    _description = "Attribute Value Group"
    _order = "attribute_id, name"

    name = fields.Char('Group Name', required=True, translate=True)
    attribute_id = fields.Many2one(
        'product.attribute',
        string="Attribute",
        required=True,
        ondelete='cascade'
    )
    value_ids = fields.Many2many(
        'product.attribute.value',
        string="Values",
        domain="[('attribute_id', '=', attribute_id)]"
    )


    @api.constrains('attribute_id', 'value_ids')
    def _check_values_attribute(self):
        for record in self:
            if any(value.attribute_id != record.attribute_id for value in record.value_ids):
                raise ValidationError(_("All values in the group must belong to the selected attribute."))
