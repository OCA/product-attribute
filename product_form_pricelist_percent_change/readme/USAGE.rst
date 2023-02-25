To use this module, you need to:

Go to Settings > Sales > Pricelist > enable pricelist and select advanced price rules (discounts, formulas).

Installing the module with this option enabled will provide a new section "Compute Selling Price" in pricelist rule form-view, with a computed field "Selling Price", an input field and a button.

- Provide a value under the button and Click the button "Set Price Discount %" to assign the percent change in the discount field.
- Selling Price field is recomputed automatically everytime a relevant dependency is changed.

Note that this feature is mostly supposed to be used by product-view form. Despite this, the feature is also available from standard Pricelist menu, but for technical reason
the new section "Compute Selling Price" will be shown only after record save (in case of newly created pricelist) and it will only be visible if the rule applies on product template or product variant.
