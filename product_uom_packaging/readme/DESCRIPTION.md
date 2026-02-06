This module provides a bridge between products, units of measure, and package types.

In Odoo 19, the `product.packaging` model was removed and packaging functionality
was merged into the UoM system. However, UoMs are shared across products, which
means you cannot specify product-specific package dimensions.

This module introduces a `product.uom.packaging` model that allows you to:

- Define which package type (with physical dimensions) applies to a specific
  product when sold/purchased in a specific UoM
- For example: "Product A in a 12-pack uses a 12x12x12 box" while
  "Product B in a 12-pack uses a 6x12x8 box"

The package type (from `stock.package.type`) provides:

- Physical dimensions (length, width, height)
- Weight limits (base weight, max weight)
- Barcode for the package type
