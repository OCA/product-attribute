.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Fixed price on pricelist rule
=============================

Adds a new option on pricelist rules to set a fixed price. This is made using
a trick that writes on the back 100% in the discount to the base price to get
a zero base that will add only the price we put in the surcharge price.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-attribute/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/product-attribute/issues/new?body=module:%20product_pricelist_fixed_price%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Ronald Portier <rportier@therp.nl>
* Giovanni Francesco Capalbo <giovanni@therp.nl>

Previous version contributors
-----------------------------

* Guewen Baconnier guewen.baconnier@camptocamp.com
* Laetitia Gangloff laetitia.gangloff@acsone.eu
* Maxime Chambreuil maxime.chambreuil@savoirfairelinux.com
* Alexandre Fayolle alexandre.fayolle@camptocamp.com
* Jay Vora(OpenERP) jvo@tinyerp.com
* Rudolf Schnapka rs@techno-flex.de


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
