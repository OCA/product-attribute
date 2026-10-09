## Lot Sequence policy

There are two ways you can configure this module through the use of
System Parameter \`product_lot_sequence.policy\`:

- "product": This is the default behaviour once you install this module.
  It's the same than in previous Odoo versions with this module
  installed, i.e. it allows to define a dedicated sequence on each
  product.
- "global": This was the default behaviour from previous Odoo versions
  when this module was not installed, i.e it will always use the same
  global sequence for every product.

If any other value is used for this System Parameter, then you will get
the default behaviour from odoo 15.0 which will look for the last lot
number for each product and will increment it.

## Automatic product sequence creation

System Parameter `product_lot_sequence.auto_create`, default "True".

When enabled, a product sequence is created automatically for products
tracked by lot or serial number. Set it to "False" to create product
sequences manually from the product form. Products without a product
sequence use Odoo's standard lot and serial numbering.

## Default Number of Digits for Product Sequence Generation

The default is 7 digits. To change that to something else, go to the
inventory configuration, find "Sequence Number of Digits" and change the
number.
