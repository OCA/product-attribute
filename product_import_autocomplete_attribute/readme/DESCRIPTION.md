This module updates the attribute lines of product templates when importing
product variants.

Natively, product template attribute values are synced from the template to its
variants, but the reverse is not true:

- the base method `product_template.create_variant_ids()` uses the template
  attributes to create the variants (template -\> variant)
- this module uses the attributes of the imported variants to update the
  attribute values of the linked template (variant -\> template)
