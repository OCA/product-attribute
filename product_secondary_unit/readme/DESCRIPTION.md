This module lets you define one or more secondary units of measure per
product (template or variant), independent of the product's own Unit of
Measure category. It solves a problem the standard multi-UoM feature
cannot: relating two units that live in **different UoM categories** and
are **not a fixed physical conversion** - for example selling a product by
weight while also tracking it in pieces, boxes, or hours, where the exact
relationship between the two can vary from one line to the next.

A secondary unit is defined by a conversion `factor` against the record's
own primary UoM, plus a `dependency_type` that controls **which direction**
that factor is allowed to drive:

- **Dependent** (the default): the two quantities stay in lock-step in
  both directions - entering one recomputes the other from the factor.
  Use it when the conversion is a fixed, reliable ratio, e.g. a product
  sold in boxes of 12 units, where the weight/quantity always equals
  `pieces × 12`.
- **Independent**: the two quantities are completely decoupled - setting
  one never touches the other. Use it when the secondary quantity is
  informational and unrelated to the primary one, e.g. selling a service
  by a fixed package (primary quantity always `1`) while also recording
  the real hours it will take to schedule an employee.
- **Secondary unit priority**: a middle ground. The primary quantity is
  still *estimated* from the secondary one through the factor (like
  "Dependent"), but the secondary quantity is **never** recomputed back
  from the primary one (like "Independent"). Use it when the secondary
  unit is the one that must stay an *exact count*, while the primary
  quantity is only ever an estimate derived from it - the canonical
  example is fish sold by weight but counted in pieces: the average
  weight per piece is just an estimate, so the piece count must never be
  silently overwritten by a weight-derived guess, while the weight is
  still usefully pre-filled from the piece count when a line is created.

Other modules build on top of this one (via the `product.secondary.unit.mixin`
this module provides) to carry the secondary unit and its quantity through
sale, purchase and stock documents - see `sale_order_secondary_unit`,
`purchase_order_secondary_unit`, `stock_secondary_unit` and related modules.
