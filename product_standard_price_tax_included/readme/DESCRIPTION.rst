In Odoo, the Cost Price Field (standard_price) is by definition 'Tax Excluded'.
So without this module, the sale price will be bad in this following configuration:

* Price list based on the field 'Cost Price';
  (If you want a fixed margin, for example: Cost Price + 10%);
* Products set with Sale Taxes "Tax Included" ; (B2C settings)

This module fixes the problem, adding a new field 'Cost Price Tax Included'
(standard_price_tax_included) on Product Template model, based on Cost Price
Field and Sale Taxes Setting.

This module create a new ``product.price.type`` item, named
'Cost Price Tax Included'.

