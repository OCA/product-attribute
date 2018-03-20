.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Product Sequence
================

This module allows to associate a sequence to the product reference.
The reference (default code) is unique (SQL constraint) and required.

You can optionally specify different sequences for different product
categories.

Installation
============

Prior to installing this module, if you have any existing products you should
ensure they already have a unique reference (or no reference) set.  Products
with a default_code of '/' or empty will automatically be assigned a code of
"!!mig!!" followed by the system id for that product.

Otherwise the setting of the unique constraint will fail and the module will
fail to install.

Usage
=====

To specify a different sequence for a product category proceed as follows:

#. Go to the a Product Category form view.
   (**note:** you will need to install Inventory app to be able to access to
   the form view, *Inventory > Configuration > Products > Products Categories*;
   or create a menuitem manually).
#. Fill the *Prefix for Product Internal Reference* as desired.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Angel Moya <angel.moya@domatix.com>
* Graeme Gellatly <g@o4sb.com>
* Sodexis <dev@sodexis.com>
* Lois Rilo <lois.rilo@eficent.com>

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
