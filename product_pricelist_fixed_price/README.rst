.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3
Fixed price on pricelist rule
=============================
Adds a new option on pricelist rules to set a fixed price. This is made using
a trick that writes on the back 100% in the discount to the base price to get
a zero base that will add only the price we put in the surcharge price.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Giovanni Francesco Capalbo <giovanni@therp.nl>
* Ronald Portier <ronald@therp.nl>
* Guewen Baconnier guewen.baconnier@camptocamp.com
* Jay Vora(OpenERP) jvo@tinyerp.com
* Laetitia Gangloff laetitia.gangloff@acsone.eu
* Maxime Chambreuil maxime.chambreuil@savoirfairelinux.com

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
