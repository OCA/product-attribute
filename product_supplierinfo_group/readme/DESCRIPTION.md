Product price values can be tedious and error-prone to enter one by one
when you need to repeat the same values:

- vendor,
- product name
- variant
- product code

Whereas most of the time you just want to enter the minimum quantities,
price, dates, delay.

With this module, price lines look to their parent
(product.supplierinfo.group) in order to get the values from these
repetitive fields.

In addition, it adds a computed field that summarizes all
price/quantities deals.

Here are some screenshots for before/after comparison.

Before: boring and error prone !

![](static/description/before.png)

After:

![](static/description/after_1.png)

Much better for the user.

![](static/description/after_2.png)

Note: do verify, when uninstalling this module: data consistency might
be altered due to some manual creation of tables/fields.
