.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Product Stock State
===================

This module add a stock state on the product in order to give an human readable
information without giving the current quantity in stock.

The state value can be :

* In Stock
* In Limited Stock (if qty available is under a threshold)
* Resupplying (if qty forcasted is > 0)
* Out of Stock (otherwise)

Configuration
=============

You can configure thresholds :

* Globally, for a company, in the Sale Settings. It will be used for all
  the products of the company.

* On product category form. It will be used for all the products of this
  category, or of the child categories. (User should be part of the new group
  'Stock State Threshold by Category'.)

* On product template form, for a specific product. (User should be part of
  the new group 'Stock State Threshold by Product'.)

Usage
=====

Go on the product tree and see the stock state

.. image:: /product_stock_state/static/description/product_product_tree.png
     :width: 800 px

Known issues / Roadmap
======================

* Company settings is in sale configuration, but it should be better on
  stock configuration. It is not possible for the time being, because
  stock.config.settings doesn't have company_id field in Odoo.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/akretion/odoo-shopinvader/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Sebastien Beau <sebastien.beau@akretion.com>
* Sylvain LE GAL <https://www.twitter.com/legalsylvain>

Funders
-------

The development of this module has been financially supported by:

* Akretion R&D
* Adaptoo
* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>
