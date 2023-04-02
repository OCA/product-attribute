UI is pretty responsive to new changes, for example you don't need to save product
record or press any button to recompute price even on newly created rules, except for rule that are based
on other pricelist. If the pricelist B depends from A, and pricelist A is a pseudo-record, you might need to save
product form to see price-recomputation.


Fields are non-stored by default. This can impact on performance so you might setup store=True for computed fields,
but keep in mind that if you have pricelist-rule A > depending on product rule for pricelist B > depending on product rule for pricelist C
and you change pricelist-rule A, B will be recomputed but C will not. This will not be an issue if you
keep computed fields non-stored.
