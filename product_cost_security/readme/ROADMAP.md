- To edit product costs, apart from having *Product costs / Edit*
  permission, you need to have some other permission that lets you edit
  products, such as *Sales / Administrator* or *Inventory /
  Administrator*.
- This module will raise an error in point_of_sale session opening if the user
  does not belong to Product Cost/Read group. The error can be fixed by
  the glue pos_product_cost_security module but we still have an incoherent
  logic : the pos users must have the cost read right to be able to see the
  products in their session which does not cover the use case where we do not
  want some pos users to see the cost informations in the backend.
  https://github.com/OCA/product-attribute/issues/556
