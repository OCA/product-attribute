.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==================================
Product Supplierinfo for Customers
==================================

This modules allows to use supplier info structure, available in
*Inventory* tab of the product form, also for defining customer information,
allowing to define prices per customer and product.

Configuration
=============

For these prices to be used in sale prices calculations, you will have
to create a pricelist with a rule with option "Based on" with the value
"Partner Prices: Take the price from the customer info on the 'product form')".

Usage
=====

There's a new section on *Sales* tab of the product form called "Customers",
where you can define records for customers with the same structure of the
suppliers.

There's a new option on pricelist items that allows to get the prices from the
supplierinfo at the product form.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/11.0

Known issues / Roadmap
======================

* Product prices through this method are only guaranteed on the standard sale
  order workflow. Other custom flows maybe don't reflect the price.
* The minimum quantity will neither apply on sale orders.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Contributors
------------
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Aaron Henriquez <ahenriquez@eficent.com>
* Miquel Raïch <miquel.raich@eficent.com>
* Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>

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
