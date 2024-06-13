This module adds a more powerful way to describe your product attributes combinations
than the default exclusions.

It allows to write rules like:

  * All products with blue or green color in XL size will appear only with a V neck collar
    and a short sleeve.
  * All L size products will never appear with a sailor collar.

The rules are split between a precondition a type and a postcondition.

Different attributes are ANDed and same attributes are ORed.

For instance the rule::

  All products with blue or green color in XL size will appear only with a V neck collar and a short sleeve.


Will be written as::

  Precondition: (color: blue), (color: green), (size: XL)
  Type: Only With
  Postcondition: (collar: V neck), (sleeve: short)
