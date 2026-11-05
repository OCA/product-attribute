This module allows to choose an Unit Of Measure (UoM) for products
weight and volume. It can be set product per product for users in
group_uom.

Without this module, you only have the choice between Kg or Lb(s) and m³
for all the products.

For some business cases, you need to express in more precise UoM than
default ones like Liters instead of M³.

Even if you choose another UoM for the weight or volume, the system will
still store the value for these fields in the Odoo default UoM (Kg or
Lb(s) and m³). This ensures that the arithmetic operations on these
fields are correct and consistent with the rest of the addons.

Once this addon is installed values stored into the initial Volume and
Weight fields on the product and product template models are no more
rounded to the decimal precision defined for these fields. This could
lead to some side effects into reportss where these fields are used. You
can replace the fields by the new ones provided by this addon to avoid
this problem (product_volume and product_weight). In any cases, since
you use different UoM by product, you should most probably modify your
reportss to display the right UoM.
