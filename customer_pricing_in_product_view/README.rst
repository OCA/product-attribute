.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Customer Pricing in Product View
================================

This module was written to extend the functionality of products and partners to add a
'Product Pricing' button to the partner view which when clicked will open the product list
with the pricelist set to the customers pricelist.

Installation
============

To install this module, you need to:

* do nothing special

Configuration
=============

To configure this module, you need to:

* do nothing

Usage
=====

To use this module, you need to:

* Access a customer record
* Click 'Product Pricing' 'smart button' in the button group on the right hand side

This will take you to a list of products, with the price column set to the customers pricelist.

* Search for products as per normal

NOTE: This is just a default, and the pricelist may be changed in the product view to view prices from a different
pricelist.


Known issues / Roadmap
======================

* In previous releases this module was called 'customer_context_in_product_view' and allowed typing in a customers name
  directly in the product view.  Unfortunately with changes to the v8 search view handling of functional many2one's
  and the deprecation of fields.Dummy this was not easily portable however it is desired to find a more elegant way
  of doing this in future. It might be possible by converting pricelist_id to a related field of a partner field and
  removing pricelist from the search view.
* It has previously been requested that this support supplier pricelists as well, however there are certain difficulties
  with that approach, not least of which is one supplier rarely supplies all products making displayed prices meaningless.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-attribute/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/product-attribute/issues/new?body=module:%20customer_product_pricing_button%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Graeme Gellatly <g@o4sb.com>
* Ronald Portier <rportier@therp.nl>

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
