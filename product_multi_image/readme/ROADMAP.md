- The field "Available in these variants" appears when opening the image
  from the product variant.
- Add logic for handling to add images with the same name that another
  variant of the same template, renaming the new image to a unique name.
- Add logic for handling to add the same image in several variants to a
  already in another variant for not duplicating bytes.
- If you try to sort images before saving the product variant or
  template, you will get an error similar to
  `DataError: invalid input syntax for integer: "one2many_v_id_62"`.
  This bug has not been fixed yet, but a workaround is to save and edit
  again to sort images.
