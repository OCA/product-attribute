.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==============
Product sale tax price included
==============

This module permits to quickly see the different prices of a product : price with taxes and price without taxes.

.. image:: /product_sale_tax_price_included/static/description/product_different_prices.png
   :alt: Product with his price and the price without taxes
   :width: 40%

The four use cases
=====

In Customer taxes, there's a boolean called "Tax included in Price".

.. image:: /product_sale_tax_price_included/static/description/taxes_creation.png
   :alt: Choice of customer taxes
   :width: 40%

**According to the customer taxes** of the product (choosen in accouting part), there are 4 possibilities :

- The sale price **AND** the sale price without taxes are displayed.

.. image:: /product_sale_tax_price_included/static/description/product_tax_included.png
   :alt: A product with sale price and sale price without taxes
   :width: 75%

- **Or** the sale price **AND** the sale price with taxes.

.. image:: /product_sale_tax_price_included/static/description/product_tax_excluded.png
   :alt: A product with sale price and sale price with taxes
   :width: 75%

- **Or** if you choose two customer taxes, one included in price, and the other one not included in price,
this module displays the sale price and the two calculated prices.

.. image:: /product_sale_tax_price_included/static/description/product_tax_included_and_not.png
   :alt: A product with sale price and a warning message
   :width: 75%

- **And lastly** if there's no taxe choosen, only the normal price is displayed. 

Credits
=======

Contributors
------------

* Quentin Dupont, GRAP <quentin.dupont@grap.coop> (http://www.grap.coop/)
* Sylvain Legal, GRAP <sylvain.legal@grap.coop> (http://www.grap.coop/)

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
