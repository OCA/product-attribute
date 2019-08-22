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
