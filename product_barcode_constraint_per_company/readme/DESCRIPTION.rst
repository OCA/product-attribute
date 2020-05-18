This module extend Odoo functionnalities changing the constraint of the barcode
on the ``product.product`` model.

With this module, two products can have the same barcode, if there don't belong
to the same company.

This contrainst was introduced in Odoo V9.0 in [that commit](https://github.com/odoo/odoo/commit/ede1071a09902e6eeb315cf51325a03f3991b3c3), and doesn't fit with some multi companies implementation where products are not shared.
