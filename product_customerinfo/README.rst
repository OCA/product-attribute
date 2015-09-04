.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

============================================
Use product supplier info also for customers
============================================

This modules allows to use supplier info structure, available in
*Procurements* tab of the product form, also for defining customer information,
allowing to define prices per customer and product.

Configuration
=============

For these prices to be used in sale prices calculations, you will have
to create a pricelist with a rule with option "Based on" with the value
"Supplier prices on the product form" (although the text is not clear enough).

Usage
=====

There's a new section on *Sales* tab of the product form called "Customers",
where you can define records for customers with the same structure of the
suppliers.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/8.0

Known issues / Roadmap
======================

* Product prices through this method are only guaranteed on the standard sale
  order workflow. Other custom flows maybe don't reflect the price.
* The product code / product name specified for the customer will not be
  reflected on the sale orders.
* The minimum quantity will not also be applied on sale orders.
* Computed fields in product.supplierinfo object won't properly work for
  customer type

Credits
=======

Contributors
------------
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
