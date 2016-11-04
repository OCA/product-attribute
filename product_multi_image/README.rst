.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Multiple Images in Products
===========================

This module implements the possibility to have multiple images for a product
template, a.k.a. an image gallery.

Installation
============

To install this module, you need to:

* Install ``base_multi_image`` from
  `OCA/server-tools <https://github.com/OCA/server-tools>`_.

Usage
=====

You can manage your images at Product template level:

#. Go to *Sales > Products > Products* and choose a product template.
#. Go to the *Images* tab.
#. Add a new image or edit the existing ones.
#. You can select for which variants you want to make available the image.
   Keep it empty for making visible in all.
#. Refresh the page.
#. The first image in the collection is the main image for the product
   template.

Going to product variants form, you can manage also your images, but take
into account this behaviour:

#. Go to *Sales > Products > Product Variants* and choose a product variant.
#. If you add an image here, the image is actually added to the product
   template, and restricted to this variant.
#. When editing an existing image, the image is changed generally for all
   the variants where is enabled, not only for this variant.
#. When removing an image from this form, if the image is only in this variant,
   the image is removed. Otherwise, the image gets restricted to the rest of
   the variants where is available.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/9.0

Known issues / Roadmap
======================

* When you change the image on the product variant, the preview image of the
  *Images* tab doesn't get refreshed until you refresh the browser, or if you
  go to its template, but the image has been actually saved!
* The field "Available in these variants" appears when opening the image
  from the product variant.
* Add logic for handling to add images with the same name that another variant
  of the same template, renaming the new image to a unique name.
* Add logic for handling to add the same image in several variants to a
  already in another variant for not duplicating bytes.
* Provide proper migration scripts from module product_images from 7.0.
* Migrate to v8 api when https://github.com/odoo/odoo/issues/10799 gets fixed.
* If you try to sort images before saving the product variant or template, you
  will get an error similar to ``DataError: invalid input syntax for integer:
  "one2many_v_id_62"``. This bug has not been fixed yet, but a workaround is to
  save and edit again to sort images.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Original implementation
-----------------------
This module is inspired in previous module *product_images* from OpenLabs
and Akretion.

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Rafael Blasco <rafabn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>
* Dave Lasley <dave@laslabs.com>

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
