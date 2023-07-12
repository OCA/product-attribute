This module provides a function to estimate the weight of a given quantity of a product,
taking into account the product packaging's weights and return the weight in the product uom.

It uses the module `stock_packaging_calculator` to get weight from product packagings
having a weight defined first and fallback on product weight field
if no weight is defined on any of the packaging.

.. warning::

  This module is lacking the weight uom conversions as it depends on
  *product_packaging_dimension* that depends on *product_logistics_uom*
  that allows to set a uom on the weight.

  **The sum in this module is assuming all weights are in kg**.
