Product Variant Default Code(product_variant_default_code)
-----------------------------------------------------------

In 'product.template' object new field 'Variant reference mask' is added

In 'product.attribute.value' object new field 'Attribute Code' is added.

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
