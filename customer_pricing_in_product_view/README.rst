.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Display Customer Price in Product View
======================================

This module extends the functionality of products and partners by
adding a button named "Pricing" on the partner view.  On clicking
it will open up a list of products displaying the customers pricing

Installation
============

While the module will install without the sale module, the functionality
won't be visible so it is expected that sale module will be installed as well.

Configuration
=============

In order for the module to be useful you will need to have enabled both
variants and advanced pricelists under the Sales / Settings menu.

Usage
=====

# Navigate to a customer (form view)
# Click the button labelled pricing.
# In the resulting tree view an extra column called price will show the customer price.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

Known issues / Roadmap
======================

* Previous versions of this module allowed the customers name to be typed directly in the view.
* While fields.dummy has been deprecated the functionality can still be acheived by an unstored many2one
on product.template in the same way as pricelist_id is currently stored.

However, the way in which the context is set presents two issues.

* The customers name rather than id is stored in context when referencing self.
* The tree view does not dynamically change context in version 10 from search bar entries.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Graeme Gellatly <g@o4sb.com>

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
