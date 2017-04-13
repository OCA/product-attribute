.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Product Variant Default Code(product_code_builder)
==================================================

This module extends the functionality of products to support setting
codes on attributes and generating specific product codes for variants

In 'product.template' object new field 'Variant reference mask' is added

In 'product.attribute.value' object new field 'Attribute Code' is added.

Installation
============

No special installation information.

Configuration
=============

No additional configuration is required.

Usage
=====

When creating a new product template without specifying the 'Variant reference
mask', a default value for 'Variant reference mask' will be automatically
generated according to the attribute line settings on the product template.
The mask will then be used as an instruction to generate default code of each
product variant of the product template with the corresponding Attribute Code
(of the attribute value) inserted. Besides the default value, 'Variant
reference mask' can be configure to your liking, make sure puting Attribut Name
inside '[]' mark.

Example:

Creating a product named 'A' with two attributes, 'Size' and 'Color'::

   Product: A
   Color: Red(r), Yellow(y), Black(b) #Red, Yellow, Black are the attribute
          value, 'r', 'y', 'b' are the corresponding code
   Size: L (l), XL(x)

The automatically generated default value for the Variant reference mask will
be `[Color]-[Size]` and then the 'default code' on the variants will be
something like `r-l` `b-l` `r-x` ...

If you like, you can change the mask value whatever you like. You can even have
the attribute name appear more than once in the mask such as ,
`fancyA/[Size]~[Color]~[Size]`, when saved the default code on variants will be
something like `fancyA/l~r~l` (for variant with Color "Red" and Size "L")
`fancyA/x~y~x` (for variant with Color "Yellow" and Size "XL").

when the code attribute is changed, it automatically regenerates the 'default
code'.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

Known issues / Roadmap
======================

* None at present

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

This module was initially a direct port of the module with the same name from the odoomrp project <http://odoomrp.com>

* OdooMRP team
* Avanzosc
* Serv. Tecnol. Avanzados - Pedro M. Baeza
* Shine IT(http://www.openerp.cn)
* Tony Gu <tony@openerp.cn>
* Graeme Gellatly <g@o4sb.com>

The module was then renamed to product_code_builder to replace that module and some functionality ported as well as
fields renmaed to match.

* Ascone
* Akretion
* Benoit Guillot
* Laurent Mignon


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
