When a product template is added to a sale order line, the configured
custom values become real attribute values. Here is an example:

1.  Create an attribute "Length (cm)"
2.  Add some values to the attribute:
    - 5
    - 10
    - Custom
3.  For the "Custom" value, enable custom and Create custom variant
    (added by this module)
4.  Create a product template "Glass" having the created attribute and
    all its values
5.  Create a sale order that includes the product template
6.  Set the value 42 for the attribute "Length (cm)"

With the above steps, this module creates:

- A new attribute value "42" for the attribute "Length (cm)"  
  This attribute value is not linked to the product template, so it does
  not appear as a choice when the template is sold.

- A variant for the template, linked to the created attribute value

The created variant can then be used to retrieve its stock quantity or
to purchase that exact product variant that had been sold.
