This module enhances the name search of product template attribute values to
support the composite "Attribute: Value" display name format.

In standard Odoo, ``product.template.attribute.value`` records display as
"Attribute: Value" (e.g., "Color: Red"), but the search only looks at the
``name`` field. This means attribute values with the same name under different
attributes (e.g., "Red" under both "Color" and "Size") cannot be distinguished
during import or name-based lookups.

With this module installed, searching for "Color: Red" will match only the
"Red" value under the "Color" attribute, enabling unambiguous matching by
display name.
