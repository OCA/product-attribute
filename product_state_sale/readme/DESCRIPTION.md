This module adds the use of the `product_state` module in Sale.

It adds a *Can Be Sold* flag on product states. Products whose state does not
allow sales are hidden from the product selection on quotations and sales
orders, and adding such a product to an order line is refused. The flag is
exposed on the product as *State Allows Sale*.
