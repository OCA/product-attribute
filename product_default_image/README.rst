.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

======================
Default Product Images
======================

This module adds default images to products with the ability to map their images to their
`Category's Image`, to a single, `Global Product Image`, or to both, `Global and Category`, where global
acts as a backup if the category has no image. You can also disable default images by choosing
`No Default Image`.

Usage
=====

There are a few notable features in this module, see below:

Post Installation
-----------------

After installation, all products with no image will be automatically changed
when you change your company's `Product Image Target` (see Stock Configuration Page).
Since the default option is `No Default Image`, your product images will remain untouched during installation.

When Will Product Images Be Automatically Changed?
--------------------------------------------------

* Product images will automatically change when you change `Default Product Image` in the stock configuration page.
* Product images will also be changed if you change the product's category in the product form. This only applies
  if the `Default Product Image` is set to `Category's Image` or `Global and Category`.
* Lastly, product images will be automatically changed if you change the image on their category's image. Again,
  only applicable if `Default Product Image` is set to `Category's Image` or `Global and Category`.

The above rules only apply to your current products that do not have an image. Products that already
have an image when installing this module will be marked as `custom` images. The images on those products will not
change unless you click the `Apply Default Image` in the product form view.

Stock Configuration Page
------------------------

* Go to `Inventory` in the top header.
* Under `Configuration`, click `Settings`.
* Under `Products` is a field, `Default Product Image`.
* `No Default Image` deletes all eligible product images.
* `Global Product Image` sets all eligible product images to the `Global Product Image` field that
  shows up below.
* `Category's Image` sets all eligible product images to their category's image.
* `Global and Category` sets all eligible product images to their category's image if that category
  has an image. Otherwise the image is set to the `Global Product Image`.

Eligible refers to products that have Auto Change Image as True, do not have an image, do not have
a custom image, or have a default image already.

Product Category Form View
--------------------------

* Image fields have been added to categories
* Changing the category's image field will also change product images that are tied to that
  category. Only applicable if `Default Product Image` is set to `Category's Image` or `Global and Category`

Product Form View
-----------------

* Go to `Inventory` in the top header.
* Under `Inventory Control`, click `Products`.
* Click on a product.
* In the product form view, you'll see in the upper left hand corner a new button which says `Apply Default Image`.
  Use this button if you want to change a custom image to a default one, or reset a default image.
* Go to a product that has a default or no image, and you'll see a new field under the `General Information` tab
  called `Auto Change Image`. Uncheck this field if you want the image not to change. When uploading a custom image
  you don't have to worry about this field. However if you want to delete a product's image and keep it from
  automatically changing, make sure to uncheck `Auto Change Image`.

All image defaults are also loaded when you create a new product.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/10.0

Known Issues / Roadmap
======================

* Refactor product.template _change_template_image method
* Centralize logic that converts the company product_image_target to the
  correct product image_type value (usually in the form of a to_type arg),
  accounting for GLOBAL_CATEGORY. Repetitive logic occurs in: product.template
  apply_default_image, product.template _onchange_categ_id,
  product.template default_get, res.company write, and product.category write methods.
* After logic is centralized, add a res.company create method overload that auto-populates
  product images.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/product-attribute/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.
* Company Default Product Image: `Image <https://openclipart.org/detail/98491/open-box>`_.

Contributors
------------

* Brett Wood <bwood@laslabs.com>

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
