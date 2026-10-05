This module makes the product forms of the Purchase app work together with
`product_cost_security`.

Without it, users without the *Product costs* permission cannot open a product
or a product variant when Purchase is installed, because the vendor price lines
use the product cost in their context.

The default unit price of a new vendor line is still the product cost, but only
for users who are allowed to see that cost. Other users get 0, as for any other
new vendor line.

The module is installed automatically when both `product_cost_security` and
`purchase` are installed.
