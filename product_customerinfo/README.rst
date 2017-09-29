.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :alt: License: AGPL-3
    :target: http://www.gnu.org/licenses/agpl-3.0.en.html

============================================
Use product supplier info also for customers
============================================

This modules allows to use supplier info structure, available in
*Inventory* tab of the product form, also for defining customer information,
allowing to define prices per customer and product.

Configuration
=============

For these prices to be used in sale prices calculations, you will have
to create a pricelist with a rule with option "Based on" with the value
"Supplier prices on the product form".

Usage
=====

There's a new section on *Sales* tab of the product form called "Customers",
where you can define records for customers with the same structure of the
suppliers.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/10.0

Known issues / Roadmap
======================

* Product prices through this method are only guaranteed on the standard sale
  order workflow. Other custom flows maybe don't reflect the price.
* The minimum quantity will neither apply on sale orders.

Credits
=======

Contributors
------------
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Aaron Henriquez <ahenriquez@eficent.com>
