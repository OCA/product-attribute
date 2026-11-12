This module allows a pricelist rule to be restricted to a specific packaging
(unit of measure) of a product, instead of always applying to the product's
base unit.

A rule that targets a single product can be given a *Packaging*. The rule is
then only taken into account when the price is computed for that packaging,
and its *Min. Quantity* is expressed in that packaging rather than in the
product base unit. Rules without a packaging keep their standard behaviour and
apply whatever the unit of measure used.

The pricelist report is extended accordingly: a product sold in several
packagings shows one price row per packaging that has its own rule.

This is a backport of the standard implementation Odoo introduces in
version 19.3, see
[odoo/odoo@d2648b1](https://github.com/odoo/odoo/commit/d2648b1d983927b5df7260a16d6d1d33c213ddeb#diff-5a563f36ffd028b0d8510c6d1339b097a5067a2247cc35c0f9bdd1fd0b5a0b0).
