This module adds a "stock state" field on the product in order to inform the user of its general stock state at a glance.

The state value can be :

* On Demand (The product is only available upon request.
  This is particularly useful when selling such products on e-commerce platforms,
  as it allows the product to be ordered regardless of its stock quantity)
* In Stock
* In Limited Stock (if qty available is under a threshold)
* Resupplying (if qty forcasted is > 0)
* Out of Stock (otherwise)
