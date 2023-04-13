* There is an issue with the use of ir.sequence with the newer version of Odoo.

Mostly, when opening the detailed operations of an assigned picking for a product
tracked by serial numbers, Odoo systematically calls `_get_next_serial` even
if there is not any serial number to generate.
Moreover, the widget allowing to generate the serial numbers will not call
the sequence but only increment the number according to the next serial,
potentially leading to a sequence that is not in sync anymore with the created
serial numbers.

cf https://github.com/OCA/product-attribute/issues/1326
