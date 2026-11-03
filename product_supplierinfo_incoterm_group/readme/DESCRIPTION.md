Glue module between `product_supplierinfo_incoterm` and
`product_supplierinfo_group`.

The incoterm is set on the vendor pricelist group and propagated to its vendor
pricelist lines. The incoterm is part of the group key: the same vendor can
have one group per incoterm for the same product, each one with its own prices.

By default, the incoterm of the group is taken from the default purchase
incoterm of the vendor.
