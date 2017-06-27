.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3
    :target: http://www.gnu.org/licenses/agpl-3.0.en.html

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
* The minimum quantity will not also be applied on sale orders.
* Computed fields in product.supplierinfo object won't properly work for
  customer type.

Credits
=======

Contributors
------------
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Julio Serna Hernández <julio@vauxoo.com>
* Yennifer Santiago <yennifer@vauxoo.com>
* Moisés López <moylop260@vauxoo.com>

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
