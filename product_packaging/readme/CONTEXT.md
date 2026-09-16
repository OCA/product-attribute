In Odoo 19.0+, packagings are handled as Units of Measures.

However, it's a nightmare to maintain product packaging-specific information. Barcodes are defined on the Unit of Measure level through an intermediate `product.uom` model, but it's difficult to see and modify and it poses a data integrity risks.

This module improves the new packagings usability by reintroducing a dedicated Packagings section on the product form.
Additionally, it offers a model to store packaging-specific information such as weight, volume, dimensions, etc.
