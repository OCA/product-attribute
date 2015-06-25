.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Product Attribute Group
=======================

This module was written to extend the functionality of product attributes to support
grouping attributes and allow you to choose a group of attributes when creating a product
rather than one at a time while giving as much flexibility as possible.  This saves having to manually
add many attributes to products, and also allows by just updating a single group to update all products using that
group.

Installation
============

To install this module, you need to:

* do nothing special

There are no expected consequences of uninstallation outside of removing all of the groups. Individual attribute
values will remain assigned to products.

Configuration
=============

To configure this module, you need to:

* do nothing, no changes are made to existing data and fields and no new dependencies are introduced.

Usage
=====

To use this module, you need to:

* Be a member of the Sales Manager security group or admin for creation, update and removal of groups (same as Variants)
* Go to Sales -> Configuration -> Product Attribute Group
* From there you can create Attribute Groups for use in the Variants tab of products by selecting
an attribute and choosing the values belonging to that group.
* When adding/removing values to/from an existing group, you must click update variants to populate those changes
to all variants using that group.
* Groups already assigned to a product template are unable to be changed to a new attribute until removed from
those variants.

In general this module is designed to work best in a scenario where a a group or group(s) of attributes are commonly
reused for a number of templates and are subject to minimal/occasional change.  In general, while it is supported, it is
not expected in general usage that attribute values will be manually added to templates as well as groups.
If using the module in this way it will work however the user experience is not as clean and a wise policy is:
either it is groups or no groups.

Variants should not be customised as updates will lose those changes.  This is Odoo's advice not mine and a sympton
of the variant implementation of v8. (In testing, while Odoo states this is the case, certainly product images remained)
While additions and removals are supported, the Odoo implementation of variants is to delete/inactivate and recreate
them on save of the product template.  For this reason additions behave more predictably than removals, which may just
be inactivated.

* The groups act as helper rather than a dictator in the variants screen.
* It is *possible* to remove individual values from a product, however as soon as the group is updated these will be readded and is not recommended.
* Conversely manually adding non-included variants is supported and these will remain after an update.
* Groups may overlap, and if overlapping groups are added to a template the effect is a Union,
i.e. if A = {1, 3, 5, 7} and B = {1, 2, 4, 6} then A ∪ B = {1, 2, 3, 4, 5, 6, 7}
* Removing a group removes its values from the template (provided they are not in an overlapping group).
* Discard is your friend.  If you see a warning, read it, and if you are unsure discard your changes.
* When you add a new value to a group and click Update Variants it will update all of your product templates that use
that group.

A number of distinct and overlapping groups within the Color attribute have been included in the demo data
for experimentation with this functionality.


Known issues / Roadmap
======================

* Within the code there are some noted github issues relating to the new API.  Primarily these are technical in detail
however one in particular, the inability to change the field calling an onchange function, leads to a clumsier than
desired user experience when mixing individual attribute values and groups. When deleting an attribute value,
from an attribute line in the variant tab of the template screen and it belongs to a variant group, the behaviour
*should* be to change nothing.  Currently it removes the attribute and pops a warning.  Subsequent updates to the group
will readd it to the template.

* This module will ultimately become part of an app designed to restore the most important functionality of
product_variant_multi* from v7 while remaining sympathetic to the v8 Odoo implementation of variants.

* Current Modules which will form part of this app are:
  - https://github.com/OCA/product-attribute/pull/70/files
    - product_attribute_code
    - product_attribute_global_item_code

* Identified remaining features to be implemented
 - individual variant costs and price history
 - individual variant weights
 - individual variant supplier information
 - search/group/filter by variant
 - bundled product_variant_multi app with configuration options for features
 - automated tests for modules

* Possible future features
 - optional dimensions (very hard)

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-attribute/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/product-attribute/issues/new?body=module:%20product_attribute_group%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

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

To contribute to this module, please visit http://odoo-community.org.
