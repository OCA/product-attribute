.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Pricelist Item Generator
========================

This module allows to create pricelist items in a bulk way,
by separate price elements and products informations. 

It avoids a lot of manual entries.


Configuration
=============

To configure this module (for non admin user), you need to:

#. Go to Settings > Configuration > Sales > Quotation and Sales > Customer Features
#. Check 'Use pricelists'

Usage
=====

To use this module, you need to:

* Go to Sales > Configuration > Pricelists > Price Items Generator.
* Create a new one filling required fields and activate it.
* Create a price item rule in 'Price items' part.
* Add 2 rows in 'Involved products'
  (i.e. one with a product and one with a category).

.. figure:: pricelist_item_generator/static/description/img1.png
   :alt: completed generator
   :width: 600 px

* Save and click on 'Synchonize with Pricelist' button.
* Click on the version link: you now see a screen like this.

.. figure:: pricelist_item_generator/static/description/img2.png
   :alt: standard pricelist populated by generator
   :width: 600 px

* It's the standard Pricelist Version screen improved by cutting rules 
  in 2 parts: the standard one (Manual rules) and the automatic created 
  by this module.

* If you want duplicate generators, you may also duplicate one2many parts
  as here 'Price items'.

.. figure:: pricelist_item_generator/static/description/img3.png
   :alt: duplicate settings on price item generator
   :width: 600 px

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/8.0


Known issues / Roadmap
======================

* Only support sales pricelist: others possible

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Icon images comes from https://icons8.com/web-app/for/all/price%20dollar

Contributors
------------

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
