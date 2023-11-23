from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    short_name = fields.Char(help="Displayed as the variant attribute name.")
    display_attribute_value = fields.Boolean(
        "Display Attribute Value on Product Variant",
        default=True,
        help="If checked, it will display the variant attribute value in the product name.",
    )
    display_attribute_name = fields.Boolean(
        "Display Attribute Name/Short Name on Product Variant",
        help="If checked, it will display the variant attribute name before its value.",
    )

    display_no_variant_attribute = fields.Boolean(
        "Display No Variant Attributes on Product Variant",
        help="If checked, it will display the no variant attribute.",
    )

    display_single_variant_attribute = fields.Boolean(
        "Display Single Variant Attributes on Product Variant",
        help="If checked, it will display the single variant attribute.",
    )


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    sequence = fields.Integer(help="Determine the display order", index=True)


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    def _get_combination_name(self):
        """Gets the combination name of all the attributes.
        If active, it will display the name or short name before its value.
        The order of the attributes is defined by the user"""
        display_ptav_list = []
        for ptav in sorted(self, key=lambda seq: seq.attribute_line_id.sequence):
            if not ptav.attribute_id.display_attribute_value:
                continue
            if not ptav.attribute_id.display_single_variant_attribute:
                if not ptav._filter_single_value_lines():
                    continue
            if not ptav.attribute_id.display_no_variant_attribute:
                if not ptav._without_no_variant_attributes():
                    continue
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
