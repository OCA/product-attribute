This module adds a "stock state" field on the product in order to inform the user of its general stock state at a glance.

The state value can be :

* In Stock
* In Limited Stock (if qty available is under a threshold)
* Resupplying (if qty forcasted is > 0)
* Out of Stock (otherwise)
