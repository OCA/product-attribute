This module provides a function to estimate the weight of a given quantity of a product,
taking into account the product packaging's weights.

It uses the module `stock_packaging_calculator` to get weight from product packagings
having a weight defined first and fallback on product weight field
if no weight is defined on any of the packaging.
