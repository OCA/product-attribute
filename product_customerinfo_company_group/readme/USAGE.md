1. Set the *Company Group* field (`company_group_id`) on a company, from
   *Contacts*, to tag it as part of a group.
2. Create a customer info record for any partner: an individual client, its
   parent company, or the company group.
3. Wherever `product.product._select_customerinfo()` is used (customer
   pricing, sale order line customer code/name, minimum quantity), the record
   returned is the one on the most specific level available for the ordering
   client: client first, then parent company, then company group.
