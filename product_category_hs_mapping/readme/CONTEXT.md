# Why this module exists

## The problem

When products land in Odoo from a supplier integration (cXML /
OCI punchout cart, REST-API enrichment, EDI feed, IDoc import,
…) they typically arrive with:

- a **customs HS code** (``commodityCode`` in the supplier's
  payload, populated on ``product.template.hs_code`` via OCA
  ``account_intrastat`` or equivalent),
- but **no product category** — or a placeholder category the
  integration uses as a landing zone (``All / Imported`` or the
  supplier-specific bucket the punchout backend defaults to).

The category drives downstream behaviour: which warehouse
location the product lands in, which procurement rules fire,
which analytic account a reorder hits, which sales tax applies,
which sequence the auto-generated internal reference uses.
Leaving thousands of imported SKUs in a single placeholder
category breaks every one of those flows.

## What this module does

A small mapping table: HS-code patterns → ``product.category``.
Designed to plug into any flow that sets ``hs_code`` on a
product:

```python
mapped = self.env["product.category.hs.mapping"]._get_category_for_hs_code(
    "84314100",        # Forks for fork-lift trucks
    company=self.company_id,
)
if mapped:
    template.categ_id = mapped
```

Patterns can be:

- **Full HS heading or subheading**: ``8431`` (parts of
  fork-lifts), ``843141`` (specific fork-lift parts),
  ``84314100`` (forks). Longer literals win — a rule with
  ``84314100`` beats a rule with ``8431`` for input
  ``8431410080``.
- **Wildcard**: ``8431*`` is identical in behaviour to
  ``8431`` (the trailing ``*`` is purely visual). The bare
  ``*`` pattern is a deliberate catch-all (specificity 0),
  matched last when nothing else fits.

Per-company scope: rules with ``company_id`` set apply only to
that company; rules with no ``company_id`` apply to all
companies. Multi-company customers can ship different mapping
tables per legal entity.

## Why it's distinct from existing OCA work

OCA already provides:

- ``account_intrastat`` — the source of HS codes themselves
  (``account.intrastat.code`` records mapped to
  ``product.template.hs_code``).
- ``account_intrastat_oss`` and friends — declaration-level
  consumers of those codes.

Neither maps HS codes to **product categories**. The closest
adjacent module, ``product_category_active``, manages category
lifecycle but doesn't classify products by HS. This module fills
the gap between "we have a customs code on the product" and "we
want the product in the right Odoo category".

## Use cases that drive this design

- **Punchout cart imports**: every line in the cart enters with
  ``hs_code`` from the supplier's cXML / OCI payload. The
  punchout-purchase glue calls
  ``_get_category_for_hs_code(hs_code)`` on the freshly created
  ``product.template`` and writes the result to ``categ_id``.
- **REST-API product enrichment** (OEM parts catalogues): when
  Odoo enriches a stub product with ``GET /items``-style data
  from the supplier, the response carries ``commodityCode``;
  same lookup populates the category at the same time.
- **EDI imports** (Pricat, custom CSV, …): an import wizard
  sets ``hs_code`` first and the category after, using the
  matcher.
- **Manual buyer override**: the bundled ``Apply HS Code →
  Category Mapping`` server action lets a buyer re-run the
  resolver against any selected product (Action menu, form +
  list view) — useful for retroactively classifying a
  pre-existing catalogue, or for debugging a rule that doesn't
  match what the buyer expected.

## Bootstrap data is *not* shipped here

The module deliberately ships **no rules**. Each customer's
mapping table reflects their own catalogue scope (different
HS chapters, different category trees, different language
preferences). A customer-side bootstrap module sits on top:

```python
"depends": [
    "product",
    "product_category_hs_mapping",
],
"data": [
    "data/product.category.csv",
    "data/product_category_hs_mapping.xml",
],
```

That bootstrap module carries the customer's ``noupdate="1"``
seed records, marked so buyer edits survive future upgrades.
Customer adoption pattern: install this matcher module from
OCA, then ship a tiny private module with your own category
tree + HS rules.
