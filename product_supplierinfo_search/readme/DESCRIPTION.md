This module lets you find a product by the supplier's code or name
(`product_code` / `product_name` defined on `product.supplierinfo`) from **any**
product search box.

Standard Odoo already matches the supplier code, but only when a supplier is
present in the context (for example, a purchase order line for that vendor).
This module removes that restriction so the same search works everywhere:
the general Products view, sale order lines, inventory operations, etc.
