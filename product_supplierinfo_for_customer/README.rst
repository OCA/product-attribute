.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3
    :target: http://www.gnu.org/licenses/agpl-3.0.en.html

============================================
Use product supplier info also for customers
============================================

This modules allows to use supplier info structure, available in
*Inventory* tab of the product form, also for defining customer information,
allowing to define prices per customer and product.

Usage
=====

There's a new section on *Sales* tab of the product form called "Customers",
where you can define records for customers with the same structure of the
suppliers.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/9.0


The product code / product name specified for the customer can be reflected
on the sale orders using module `product_supplierinfo_for_customer_sale
<https://github.com/OCA/product-attribute/tree/9.0/product_supplierinfo_for_customer_sale>`_

Known issues / Roadmap
======================

* In Odoo v9.0, it was removed the option to create pricelist based on supplierinfo prices.
  This feature will be added in the v10 of this module.
* Product prices through this method are only guaranteed on the standard sale
  order workflow. Other custom flows maybe don't reflect the price.
* The minimum quantity will not also be applied on sale orders.
* Computed fields in product.supplierinfo object won't properly work for
  customer type.

Credits
=======

Contributors
------------
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Aaron Henriquez <ahenriquez@eficent.com>
