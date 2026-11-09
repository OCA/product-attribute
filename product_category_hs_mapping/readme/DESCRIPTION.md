Maps customs HS (Harmonized System) tariff codes to Odoo
`product.category` records, so EDI / supplier integrations can
auto-categorise newly-created products without hard-coding mapping
logic per integration.

The mapping table supports two pattern shapes:

- **Exact code** — e.g. `8421230090` matches only that exact code.
- **Prefix wildcard** — e.g. `8421*` matches any code starting with
  `8421`.

At resolution time, the longest literal prefix wins. So a rule for
`8421230090` (specificity 10) beats a rule for `8421*` (specificity
4) which itself beats `84*` (specificity 2).

Multi-company aware: rules can be scoped to a specific company or
left global (apply to all companies).

Ships with a sensible default mapping table covering common
spare-parts HS chapters relevant to material-handling and
industrial-equipment maintenance. Customers will typically redirect
the targets to their own product-category tree.
