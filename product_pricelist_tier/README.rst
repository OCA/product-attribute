.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Product Pricelist Tier
======================

This module extends pricelist items with a new type called tiered, allowing users to set
a desired price at a defined minimum quantity. The price discount will be automatically
calculated to achieve that desired price, and orders of minimum quantity or greater will
have the price discount applied on them.

Usage
=====

* Ensure the 'Sale Price' setting is set to 'Advanced pricing based on formulas . . . ' in the Sales app.
* In the pricelist form view, click 'Edit'.
* Click on one of the pricelist items.
* Set 'Apply On' To 'Product' and choose a product.
* Set 'Compute Price' to 'Tiered Price'.
* In the field that shows up below 'Tiered Price', input your desired price at 'Minimum Quantity' you specify.
* Notice the 'Price Discount' field automatically changes. The logic divides your desired price by the minimum quantity
  to get the new unit price, and then compares that unit price with the original unit price of the product to achieve the price discount.
* Note the tiered pricing uses the product's Public Price, or in field terms, list_price, for calculations.
* Also note, in certain situations (e.g. $10 tiered price for 3 items) you may need to use the rounding methods available.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/vertical-medical/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Brett Wood <bwood@laslabs.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
