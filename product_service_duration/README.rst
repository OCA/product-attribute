.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

========================
Product Service Duration
========================

Extension of products (services only) that allows them to be added to calendars.

As a note, if you add services with a `Minimum Time` (minimum time it
takes to complete that service) to an event, the meeting/event duration cannot
be less than the combined minimum time of those services.

For example, say your meeting involves two services, technical and design services.
If the technical service requires 2 hours and design requires 3 hours, then your
meeting must be at least 5 hours.

The above constraint does not apply on events that have `All Day` selected.

When changing the `Minimum Time` on services, this will not affect events that have
already ended.

Usage
=====

To use this module:

* Click the `Sales` tab in the top navigation, and go to `Settings`.
* Set `Product Variants` to `Products can have several attributes . . .`
* In the left panel, click on `Product Variants`.
* In the form view there, you'll see resources and minimum service times added.
* Calendar views also have products and minimum event durations added.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

Known Issues / Roadmap
======================

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

* Brett Wood <bwood@laslabs.com>

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
