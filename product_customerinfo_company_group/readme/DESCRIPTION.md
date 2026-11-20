Module bridging product_customerinfo (OCA/product-attribute) and
base_partner_company_group (OCA/partner-contact): it makes customerinfo
lookups fall back from the client to its parent company and then to its company group.

`product_customerinfo` (OCA/product-attribute) already looks up a customer's
info on the client itself, its parent company and its commercial partner, but
as a single flat match with no order of precedence between the three.

This module turns that lookup into a real hierarchy, checked in order:

1. the client itself;
2. its parent company (`parent_id`);
3. its company group (`company_group_id`, from `base_partner_company_group`
   in OCA/partner-contact).

The first level with a matching customerinfo record wins. A record set on
the client always overrides one set on the parent company or the company
group, while the company group can still hold a single record shared by
every company and contact under it.
