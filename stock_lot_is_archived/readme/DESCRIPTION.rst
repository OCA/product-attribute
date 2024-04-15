This module allows to adds a field on lots that means a product is archived.
This differs from Odoo core 'active' attribute (see `stock_production_lot_active` module).
A cron is also provided to automatically archive lots when there is new one,
based on the expiration date.
