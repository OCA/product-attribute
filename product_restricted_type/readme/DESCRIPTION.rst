This module adds 'restricted_product_type' to product_category model.
With this optional selection field 'restricted_product_type' should
have the same values as in the product.template, 'type' field.

A constrain is also established in the product so that when the 'type'
defined in the product does not match with the 'restricted_product_type'
defined in the product category it raises a Validation Error.

Also, in the product category one would not be able to change the field
'restricted_product_type' if the category has been assigned at least to
one product that already has this category, but has a different 'type' value.