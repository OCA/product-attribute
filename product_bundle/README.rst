.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============
Product Bundle
==============

This module extends the functionality of products to support having a bundle of
products in a single one.

Internally, bundles will always be consumable products, but you will be able to
see their stock, which is extracted from the maximum amount of stockable
products' stock.

For example, if your bundle includes 2 RAM, 1 Graphic card and 1 hour of work,
and your stock of RAM is 5 and your stock of Graphic cards is 3, your bundle's
stock will be 2 (because ``min(5 // 2, 3 // 1)`` is 2).

Usage
=====

To create a product bundle, you need to:

#. Go to *Sales > Products > Products*.
#. Create a product.
#. Name it.
#. Enable the *Is bundle* check box.
#. Go to the new *Bundle* tab.
#. Add the products that form this bundle, with their quantity.
#. Return to *General Information* tab.
#. Use the *Bundled products public price* field as a hint of what price you
   want for the bundle, and set the *Sale price*.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/9.0

Known issues / Roadmap
======================

Currently bundles cannot have variants.

This is affected by https://github.com/odoo/odoo/issues/10799, and will need
some refactoring for v10.

In a bundle product form, pressing buttons *On Hand* or *Forecasted* will lead
to an empty page. What should happen is that you should not be able to press
them, because the bundle stock is computed in a special way, explained above,
but bug https://github.com/odoo/odoo/issues/13264 does not allow us to disable
the button. It should work when that bug gets fixed.

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

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Jairo Llopis <jairo.llopis@tecnativa.com>

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
