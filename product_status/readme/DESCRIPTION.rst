This module compute a status on product based on some date field
displayed on the Sales tab.
This module will deactivate all default state in product_state,
implement new default data
The option to use the product-attribute/product_state module was
considered but because the status is computed based on today. It does
not work well with a stored fields and also means there is no need for
creation of state from the user.

By order of importance, the status is computed by:
- *End-of-life*
- *Discontinued until*
- *New until*

*End-of-life* has priority over the other dates.
*Discontinued-until* has priority over *New until*.
