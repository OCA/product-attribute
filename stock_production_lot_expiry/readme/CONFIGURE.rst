
The field to use to fill the 'Expiry date' can be configured a 2 levels:

 * on the product category
 * on the product itself

The name of the field to use for a product is determined as follow:

If the field name is specified on the product, we use this. Otherwise we go
through the category hierarchy until the field name to use is defined. If the
field name is not defined by the category hierarchy we take the one defined
by the config parameter `stock_product_lot_expiry.field_name` (default 'removal_date').
This configuration is available into stock configuration from.

