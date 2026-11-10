Basic module providing an helper method to calculate the quantity of
product by packaging.

In Odoo 20.0, product variants can have their own extra packagings
(`Extra Packagings` on the variant), so the module now considers them
along with the packagings of the product template.

Since Odoo 19.0, packagings are units of measure (`uom.uom`) linked to
the product, with optional barcodes per company (`product.uom`). The
packaging records given to the context hooks (`_packaging_filter`,
`_packaging_name_getter`, `_qty_by_packaging_as_str`) and the returned
`id` values are therefore `uom.uom` records instead of
`product.packaging` ones.
