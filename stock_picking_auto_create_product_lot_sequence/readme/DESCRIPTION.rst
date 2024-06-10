This module acts as a bridge between the stock_picking_auto_create_lot and product_lot_sequence modules.
Due to the changes introduced in this commit(https://github.com/OCA/stock-logistics-workflow/commit/1f1d1cd4ba102f35971c074ca869ed6f7113cd2b)
for stock_picking_auto_create_lot, using these two modules together disrupts the design of product_lot_sequence by not allowing the use of specific
sequences for each product. This module restores the intended behavior.
