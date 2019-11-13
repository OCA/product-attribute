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