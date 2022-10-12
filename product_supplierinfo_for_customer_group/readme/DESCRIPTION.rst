If you install product_supplierinfo_for_customer and then product_supplierinfo_group
"Customer Pricelist" model behaviour will be broken, because product_supplierinfo_group
changes product.supplierinfo model fields definitions, making it related to
"Supplierinfo group".

This module restores default product.supplierinfo fields definitions and makes
product_supplierinfo_group compatible with product_supplierinfo_for_customer.

This module does not implement the features of product_supplierinfo_group compatible in
product_supplierinfo_for_customer.
