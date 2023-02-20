This module is an extension of product_form_pricelist that will introduce following features:

- Full access to product pricelist rule form-view by product form-view. A section "Compute Selling Price" will be added to the
  pricelist rule form-view


-  A computed field 'Selling Price' shows the selling price for active product template or variant depending on provided parameters


- Percent change: a button "Set Price Discount %" will be added to rule form as well. It will allow to compute the percent change
  depending on Selling Price (recomputed on button click) and a User Input field which will represent the new selling price.
  Percent change formula:

     (user input - selling price computed) / selling price computed x 100

  The result will be stored in Price Discount field or Percent Price
  depending on "Compute Price" parameter.


***********

To use this module, you need to:

Go to Settings > Sales > Pricelist > enable pricelist and select advanced price rules (discounts, formulas).

In the product form-view, click the 'Sales tab' in 'Fixed Price' section (which is not fixed price anymore..todo rename it)
and add rule based on formula. You can choose sale price, cost or other pricelist.

You can see the selling price recomputing automatically. You will also find a user input and a button "Set Price Discount".

Provide an input and click button to setup the price % discount based on percentage change between computed
selling price (based on supplierinfo price) and your input value.

Additional notes:

Note that this feature is mostly supposed to be used by product-view form. Despite this, the feature is also available from standard Pricelist menu, but for technical reason
the new section "Compute Selling Price" will be shown only after record save (in case of newly created pricelist) and it will only be visible if the rule applies on product template or product variant.


*********

Attitional notes:

UI is pretty responsive to new changes, for example you don't need to save product
record or press any button to recompute price even on newly created rules, except for rule that are based
on other pricelist. If the pricelist B depends from A, and pricelist A is a pseudo-record, you might need to save
product form to see price-recomputation.


Fields are non-stored by default. This can impact on performance so you might setup store=True for computed fields,
but keep in mind that if you have pricelist-rule A > depending on product rule for pricelist B > depending on product rule for pricelist C
and you change pricelist-rule A, B will be recomputed but C will not. This will not be an issue if you
keep computed fields non-stored.

