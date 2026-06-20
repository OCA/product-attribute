This module ensures accurate weight calculation on stock operations and delivery packages
when product variants have no weight defined.

By default, Odoo uses the variant weight on stock moves and delivery wizards.
If a variant weight is 0, the total picking weight is silently set to 0, even when
the product template has a weight defined.

This module fixes this behavior by falling back to the template weight when the variant
weight is 0, ensuring correct weight calculation on:
- Stock moves (``stock.move``)
- Delivery package wizard (``choose.delivery.package``)
