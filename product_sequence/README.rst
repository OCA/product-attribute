A module that adds sequence to the product.
===========================================

This module allows to associate a sequence to the product reference.
The reference (default code) is unique (SQL constraint) and required.

Installation
============

Prior to installing this module, if you have any existing products you should ensure
they already have a unique reference (or no reference) set.  Products with a default_code of
'/' or empty will automatically be assigned a code of "!!mig!!" followed by the system id for that product.

Otherwise the setting of the unique constraint will fail and the module will fail to install.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-attribute/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/product-attribute/issues/new?body=module:%20product_sequence%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Angel Moya <angel.moya@domatix.com>
* Graeme Gellatly <g@o4sb.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
