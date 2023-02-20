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
