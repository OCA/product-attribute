## 19.0.1.0.0 (2026-05)

- Initial OCA-bound release. Provides:
  - ``product.category.hs.mapping`` model with HS-code-pattern
    → ``product.category`` rules (longest-literal-prefix wins,
    optional ``*`` wildcard, per-company scope, security ACL).
  - ``intrastat_description`` computed Char on each rule —
    3-tier lookup (exact → shortest extending → parent prefix)
    against the installed ``account.intrastat.code`` records, so
    buyers can sanity-check what a pattern actually covers
    without reaching for a tariff manual.
  - ``Apply HS Code → Category Mapping`` server action on
    ``product.template`` (Action menu, form + list). Re-runs the
    matcher against the product's ``hs_code`` and writes the
    result to ``categ_id``. Single-product invocations raise a
    specific ``UserError`` for each "nothing happened" reason
    (no HS code / no rule / already in matched category).
    Multi-product invocations show a summary toast with the
    breakdown and a ``soft_reload`` so the list refreshes.
- Pre-OCA development was driven by a real-world customer
  deployment with a multi-thousand-SKU parts catalogue; the
  matcher graduated to OCA-shape after several rounds of
  buyer testing.
