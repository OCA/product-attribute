This module adds an incoterm on vendor pricelists (`product.supplierinfo`).

The same vendor may quote different prices for the same product depending on
the incoterm (EXW, FCA, DAP...). This field records the incoterm the price
applies to.

By default, the incoterm is taken from the default purchase incoterm of the
vendor (field added by `purchase_partner_incoterm`). It can be changed on each
vendor pricelist line.
