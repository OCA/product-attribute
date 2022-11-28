This module extends the functionality of 'Products Expiration Date'
(product_expiry) to easily detect expired lot.

It adds one new field on the Lot/Serial model.

* Expiry date (expiry_date)

The 'Expiry date' is a field filled at te creation of a lot/serial with the date
on which the lot/serial is expired. This field is filled from one of the
date fields present on the lot/serial ( 'end of life' or 'best before date' or
'removal date' or 'alert date' or ...). The field to use can be configured at
the product level or the category level.

The existing 'product_expiry_alert' field is computed accordingly.

It also allows you to easily search for expired lots.
