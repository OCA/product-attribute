Although product template attribute choices are synced from template to product variant, the reverse is not true.

In other words,

* Base function product_template.create_variant_ids() uses product template's product.attribute to create variants (tmpl->variant)
* Inversely, this module uses the product.attribute on variants, to update product.attribute on the product template (variant->tmpl)

This product.attribute sync is triggered when you do an import of product variants.
