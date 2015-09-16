.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Brings a Cost Price Field Tax Included on Product Model
=======================================================

In Odoo, the Cost Price Field (standard_price) is by definition 'Tax Excluded'.
So without this module, the sale price will be bad in this following configuration:

* Price list based on the field 'Cost Price';
  (If you want a fixed margin, for example: Cost Price + 10%);
* Products set with Sale Taxes "Tax Included" ; (B2C settings)

This module fixes the problem, adding a new field 'Cost Price Tax Included'
(standard_price_tax_included) on Product Template model, based on Cost Price
Field and Sale Taxes Setting.

This module create a new 'product.price.type' item, named
'Cost Price Tax Included'.

Usage
=====

User can now set Price List based on this field:

.. image:: /product_standard_price_tax_included/static/description/pricelist.png
   :width: 100%

The new field is displayed on the product template form:

.. image:: /product_standard_price_tax_included/static/description/product_template.png
   :width: 100%

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/8.0

For further information, please visit:

* https://www.odoo.com/forum/help-1


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-attribute/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/product-attribute/issues/new?body=module:%20product_standard_price_tax_included%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
