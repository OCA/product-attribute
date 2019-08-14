To use this module, you need to:

#. Go to *Sales > Products > Products*, create a product and set "Is Pack?".
#. Then set the products has to include in the product pack of the product.
#. Set *Pack Type*.

`Product pack` is a base module for `sale_product_pack` and others modules that
needs to use packs. `Pack type` is used to define the behavior that the
packs will have when it is selected in the sales order lines
(if `sale_product_pack` module is installed). The options of this field are the
followings:

  * Detailed - Components Prices: will show each components and its prices,
    including the pack product itself with its price.
  * Detailed - Totalized Price: will show each component but will not show
    components prices. The pack product will be the only one that has price
    and this one will be the sum of all the components prices.
  * Detailed - Fixed Price: will show each components but will not show
    components prices. The pack product will be the only one that has price
    and this one will be the price set in the pack product.
  * None Detailed - Totalized Price: Will not show the components information,
    only the pack product and the price will be the sum of all the components
