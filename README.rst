Product Variant Default Code(product_variant_default_code)
-----------------------------------------------------------

#. In 'product.template' object 'variant_reference mask' field is added

#. In 'product.attribute.value' object is added the new field
        'Attribute Code'.

#. Reference mask is automatically created according to the attribute 
        line settings on the product template. The mask can be changed
        adaptively later on and the default code for vaiants will be
        generated accodingly.

#. Reference code field of product is calculated automatically, taking as
        the value of the new field 'Attribute Code'.

