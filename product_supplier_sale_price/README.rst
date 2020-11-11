.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Product Supplier Sale Price
================

Supplier can suggest a sale price, if filled in a product instance, it can used as sale price. This module depends on product_variant_sale_price to be compatible with the price exported to Prestashop using connector_prestashop_catalog_manager

If there are more than one supplier for one product, there is a system parameter to decide how to compute the sale price: Getting the maximum, the minimum or compute an average of all of them. 

Usage
=====

* Go the Setting->System parameters
* Set a computation mode of the supplier sale price.
* Go to a Product->Suppliers
* Set the price suggested by the supplier
* Check the checkbox "Use Supplier Sale Price" for this product instance.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Marc Poch <mpoch@planetatic.com>


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
