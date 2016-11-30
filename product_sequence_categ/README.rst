Product Reference by Category Sequency [product_sequence_categ]
=================================================================

This module allows odoo users to easily manage diferente product
references sequences. You can set the sequence at 
product category then when you create a new product for this 
category product referece will be filled by the selected category.

eg:
All products
All products / Seallable : ref S , sequence 000, next 1
All products / Seallable / Computers : ref S001, sequence C000, next 1 
All products / Seallable / Printers : ref S002, sequence P000, next 1

Product:
DELL XPS - ref S001C001
Printer EPSON TP - ref S002P001

Installation
============

To install this module, you need to:

 * git clone https://github.com/OCA/product_attribute --branch 7.0
 * make it available to odoo by adding its location to the addons_path in 
   /etc/odoo-server.conf

Configuration
=============

To configure this module, you need to:

 * Wou have to fill sequence prefences at product category

Usage
=====

To use this module, you need to:

 * go to the product category and set sequence and reference.

For further information, please visit:

 * https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Rodolfo Bertozo <bertozo@kmee.com.br>
* Luis Felipe Miléo <mileo@kmee.com.br>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
