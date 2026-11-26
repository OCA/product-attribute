In Odoo 18, the *Cost* of a product valued in FIFO is the average cost of
what is left in stock. Pricing on that cost no longer follows the lots
actually sold: with 20 units bought at 10 and 20 at 15, the cost is 12.5,
while the next 20 units sold cost 10.

This module adds a new "Based on" option to pricelist rules: **FIFO Cost
(oldest lot in stock)**. The base price is the unit cost of the oldest stock
valuation layer with quantity left, that is the lot a FIFO delivery takes
next. When nothing is in stock, the product cost is used, as with the *Cost*
base.
