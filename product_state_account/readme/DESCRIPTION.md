This module adds the use of the `product_state` module in Invoicing.

It adds a *Can Be Invoiced* flag on product states. Products whose state does
not allow invoicing are hidden from the product selection on customer
invoices, credit notes and receipts, and adding such a product to an invoice
line is refused. Vendor bills are not restricted. The flag is exposed on the
product as *State Allows Invoicing*. The check uses the state of the
product variant, so variant-specific states (e.g. with `product_status`) are
honoured.
