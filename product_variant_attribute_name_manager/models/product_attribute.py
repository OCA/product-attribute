from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    short_name = fields.Char(
        "Short Name", help="Displayed as the variant attribute name."
    )
    display_attribute_name = fields.Boolean(
        "Display Attribute Name on Product Variant",
        help="If checked, it will display the variant attribute name before its value.",
    )


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    sequence = fields.Integer(
        "Sequence", help="Determine the display order", index=True
    )


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    def _get_combination_name(self):
        """Gets the combination name of all the attributes.
        If active, it will display the name or short name before its value.
        The order of the attributes is defined by the user"""
        display_ptav_list = []
        for ptav in sorted(
            self._without_no_variant_attributes()._filter_single_value_lines(),
            key=lambda seq: seq.attribute_line_id.sequence,
        ):
            if ptav.attribute_id.display_attribute_name:
                if ptav.attribute_id.short_name:
                    display_ptav_list.append(
                        "%s: %s" % (ptav.attribute_id.short_name, ptav.name)
                    )
                else:
                    display_ptav_list.append(
                        "%s: %s" % (ptav.attribute_id.name, ptav.name)
                    )
            else:
                display_ptav_list.append(ptav.name)
        return ", ".join(display_ptav_list)
