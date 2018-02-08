.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
Product alert when close to End-of-Life(Eol) Date
=================================================

This module allows you to set the End of Life Date of a Product.

Products with EoL Date in the past are excluded from the list of Products in Purchase Order so the product can not be ordered.

A scheduled action is created to know in advance the list of products whose EoL Date is approaching.
An email will be sent to the members of the Discussion Channel for Product Eol Notification Group.

Configuration
=============

Discuss Channel
---------------

* Look for the the Private Channel > Product End-Of-Life Channel.
* Click settings and add members on this channel.

Scheduled Action
----------------

* The scheduled action is already configured to check
  if a product is about to reach its end-of-life
* The interval is automatically configured using the notification delay setting

Notification Delay
------------------

* The delay before a notification is sent for a product about to reach its end-of-life
  can be configured in Inventory > Configuration > Settings

Usage
=====

Products
--------

* Go to Inventory > Master Data > Products
* Create or edit a product
* Enter the End of Life Date and save

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

* Antonio Yamuta <ayamuta@opensourceintegrators.com>
* Patrick Tombez <patrick.tombez@camptocamp.com>

Funders
-------

The development of this module has been financially supported by:

* Open Source Integrators <http://www.opensourceintegrators.com>

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
