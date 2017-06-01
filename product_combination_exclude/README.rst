.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Product Combination Exclude
===========================

Allows the specification of incompatible product combinations when creating products.

Sometimes certain combination of products are incompatible, yet we still wish to use the power
of variants to manage products.  With this module you can specify incompatible combinations,
assign them globally or just to selected templates, generate the list of exclusions and then even
manually fine tune them if you choose before updating the associated products.

Installation
============

There are no special installation instructions for this module.

Configuration
=============

To configure this module, you need to:

#. Enable product variants under the Sales / Configuration / Settings menu if not already the case.

Usage
=====

To use this module, you need to:

#. Go to Sales / Settings / Products / Attribute Exclusions.
#. Click Create to create a new exclusion matrix.
#. Give the matrix a name and optionally a description.
#. Add the list of values which are incompatible.  The values can be from any attribute.
#. Add the product templates to which these exclusions apply, or leave blank to apply to all.
#. Click create exclusions to automatically generate the incompatible combinations.
#. Optionally, manually edit the automatically generated list (will be overwritten every time create exclusions is clicked).
#. If not applying globally, click update products and the listed templates will be updated to remove/deactivate incompatible variants.
#. If applying globally to all templates, then you must trigger the creation of variants on the product.

To better understand consider the situation in which Red and Green T-Shirts are available in all sizes except Large.
#. We use T-Shirts as our Product Template.
#. Red, Green and Large are our incompatible attributes.
#. Generating exclusions gives us 2 lines.

Updating products means that any T-Shirts that have both the large and either green or red color are no longer available.
This is regardless of any 3rd attribute, such as logo.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* Currently no easy way to apply global exclusions to all affected templates.

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
