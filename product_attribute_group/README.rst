.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Product Attribute Group
=======================

Allows grouping of product attributes for easy addition to a product template.  It is
designed for environments where large number of products share attributes and are managed
in a systematic manner.  It allows you to maintain variants by simply changing the attribute
groups values or adding a group to an existing product.

For example you may have an attribute Color which contains many colors.  Many products
may be available in the same colors, while others may be available in a different set of
colors.  By creating 2 seperate attribute groups the values can be automatically
populated when assigned to a product.

While simple, this module is extremely powerful, allowing product administrators to
quickly add, update and delete large number of products.  Before using in production
please read this documentation thoroughly, consider running in a test environment and
review security for the users that can access.

Installation
============

No special installation requirements for the simple case.

For larger installations, where you have a large number of (potential) variant
combinations or attribute groups which will be assigned to many products, it is
recommended to run an odoo process on a seperate port with --workers=0 set and
work with attribute groups on this process to avoid timeout issues.

Configuration
=============

To configure this module, you need to:

#.    Go to Sales / Configuration / Settings and ensure that product variants is enabled.
#.    Existing installations using variants may need extra configuration depending on need. Attribute groups may need to be created and added to existing templates. Where no attribute group exists values may be added individually.

Usage
=====

To use this module, you need to:

Creating attribute groups
-------------------------
#. Go to Sales / Configuration / Products / Product Attribute Groups
#. Click Create to create a new group
#. Give it a name, assign it to an existing product attribute and then add values

The attribute group can now be used to quickly add values to products.  It is important when structuring groups
that they are meaningful to the range of products they are assigned to and not
merely convenient. A change to an attribute group affects all assigned products and an attribute line
can be assigned more than one attribute group.

Adding to products
------------------
#. Go to Sales / Products
#. Open or create the product you wish to add an attribute group to.
#. Add the attribute groups to the attribute lines under variants.

You will see your values pulled back automatically.  Note it is not possible to
add individual values when using attribute groups, however multiple groups can be assigned to a
single line.

Updating attribute groups
-------------------------
Over time the range of attribute groups may change.
Adding or deleting values from an attribute group will update all products
with this group.  It follows the standard product heuristics for deletion, inactivating
products with existing references.

Duplicating attribute groups
----------------------------
You may duplicate attribute groups using the copy button in the Product Attribute Group view
and these will be given the same name with (Copy) appended.  The new group will
have the same values but will not be assigned to any products.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* You cannot combine manually added values with attribute groups.  This was a design decision in order to keep the module simple and compatible with known modules.

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
