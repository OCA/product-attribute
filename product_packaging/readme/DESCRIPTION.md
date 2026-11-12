This module brings back a clear **Packagings** section on product forms.

With it, you can:

- Define the additional units used to sell or handle a product (for example box, case, or pallet).
- Set a **barcode for each packaging on each product variant** (useful for scanning and logistics).
- Manage everything from the product form, in one place, with a layout closer to what users knew in Odoo 18.

Packaging units are defined once per product template and shared by all its variants. Barcodes remain specific to each variant.

## Technical note

The module reimplements the UX to configure the packagings on the product forms, but it's built on top of Odoo's new packaging mechanics using the Unit of Measure model.
The `product.packaging` model is used as a proxy to configure the lower-level `product.template.uom_ids` and its `product.uom` records for the packaging barcodes.
It also implements additional fields on the packaging level to compute and store the package weight, volume, etc..
