.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Product Pack
============

This module extends the functionality of products to support having a
collection of products in a single one.

Product pack types
==================

This module defines the following product pack types, that will change how is
the product shown in the sales order.

Assuming *Pack* is the product pack and *subproducts* are those set to form
the *pack*, these are your pricing options:

Detailed Component Prices
-------------------------

This will show 1 line per *subproduct* and 1 line for the *pack*.

The *pack* line will cost the price set in the pack product.

The *subproducts* lines will cost the price set in each subproduct product.

Detailed Totalized Price
------------------------

This will show 1 line per *subproduct* and 1 line for the *pack*.

The *pack* line will cost the sum of the *subproducts*' prices. Do not set a
price for the pack product, it will be ignored.

The *subproducts* lines will cost zero.

Detailed Fixed Price
--------------------

This will show 1 line per *subproduct* and 1 line for the *pack*.

The *pack* line will cost the price set in the pack product.

The *subproducts* lines will cost zero. Their prices will be ignored.

Not Detailed Totalized Price
----------------------------

This will show 1 line for the *pack*.

The *pack* line will cost the sum of the *subproducts*' prices. Do not set a
price for the pack product, it will be ignored.

Not Detailed Assisted Price
---------------------------

This will show 1 line for the *pack*.

The *pack* line will cost the sum of the *subproducts*' prices, and will have a
button for editing its details. Do not set a price for the pack product, it
will be ignored.

Usage
=====

To create a product pack, you need to:

* Go to *Sales > Products > Products*.
* Create a product.
* Name it.
* Enable the *Pack* check box.
* Choose the *Pack Type*.
* Go to the new *Pack* tab.
* Add the products that form this pack, with their quantity.

To sell a product pack, you need to:

* Go to *Sales > Sales > Sales Orders*.
* Create a new one.
* Choose the *Customer*.
* *Add an Item* to products list.
* Choose the product pack you just created.
* Press *Save*.
* You will notice the sales order gets updated according to the pack type.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
product-attribute/issues/new?body=module:%20
product_pack%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Àngel Àlvarez
* Juan José Scarafía <scarafia.juanjose@gmail.com>
* Rafael Blasco <rafabn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>

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
