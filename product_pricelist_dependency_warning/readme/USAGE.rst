This module is useful in this simplified use-case:

#. Create a **base** pricelist with a global price rule
#. Create a **discount** pricelist with a global price rule, using a formula based on **base** and a discount.
#. Change the global price rule in **base**

Now the pricelist **discount** will show a warning telling you that the base price of some rules has changed.
This pricelist can also be found with the filter **Base price changed** in the pricelists list.

Uncheck **Base price changed** on the affected price rules to get rid of the warning.
