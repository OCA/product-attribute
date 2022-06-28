Product price values can be tedious and error-prone to enter one by one when you need to repeat the same values:

* vendor,
* product name,
* variant
* product code

Whereas most of the time you just want to enter the minimum quantities, price, dates, delay.

With this module, price lines look to their parent (product.supplierinfo.group) in order to get the values from these repetitive fields.

In addition, it adds a computed field that summarizes all price/quantities deals.

Here are some screenshots for before/after comparison.

Before:

.. figure:: static/description/before_1.png
   :width: 600 px

Boring and error prone !

.. figure:: static/description/before_2.png
   :width: 600 px

After:


.. figure:: static/description/after_1.png
   :width: 600 px

Much better for the user.

.. figure:: static/description/after_2.png
   :width: 600 px

Note: do verify, when uninstalling this module: data consistency might be altered
due to some manual creation of tables/fields.
