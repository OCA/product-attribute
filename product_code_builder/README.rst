.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Product Code Builder
====================

This module creates a Internal Reference (default_code) from values in variant's attributes.


Usage
=====

Create code with attributes (like memory, color, wifi).

Attributes order is preserved while code creation.


.. image:: product_code_builder/static/description/img_0.png

|

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/8.0

|

Configuration
=============


- Set 'code' field in attributes and attributes values models for code creation.
- Set sequence in attribute model to defined product varaiant code attribute order.


.. image:: product_code_builder/static/description/img_2.png


|
|


- Automatic Reference behavior can be turn off by uncheck on product template. 
- Internal Reference Prefix can be defined on product template.


.. image:: product_code_builder/static/description/img_1.png


|

Warning
=======

This module may be not compatible with other modules which manage default_code like product_sequence


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/product-attribute/issues/new?body=module:%20
product_code_builder%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Known issues / Roadmap
======================

MIGRATION INSTRUCTION: Some fields in this module are the same than those in 
product_attribute_priority module. For v10 or v9, it's required to add 
dependency between these modules.


Credits
=======

Contributors
------------

* Benoît GUILLOT <benoit.guillot@akretion.com>
* Abdessamad HILALI <abdessamad.hilali@akretion.com>
* David BEAL <david.beal@akretion.com>


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
