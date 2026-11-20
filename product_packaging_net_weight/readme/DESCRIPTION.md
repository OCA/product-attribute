This is a glue module between `product_packaging` and `product_net_weight`.

It adds the net weight on product packagings, seeded from the product net
weight scaled by the packaging quantity, similarly to how the gross weight is
handled by `product_packaging`.

It is auto installed when both modules are installed.
