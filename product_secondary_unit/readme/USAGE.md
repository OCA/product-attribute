## Defining a secondary unit on a product

1.  Enable *Settings \> Units of Measure* (this module's field is only
    shown when the `uom.group_uom` feature is active).
2.  Go to a product's *General Information* tab. A *Secondary Unit of
    Measure* section lists any secondary units already defined for it.
3.  Add a line: pick a *Secondary Unit of Measure* (a standard Odoo UoM,
    e.g. `Units`), a *Secondary Unit Factor*, and a *dependency type*.
    Optionally restrict the line to one specific variant instead of the
    whole template.
4.  A product can have several secondary units at once (e.g. "box of 5"
    and "box of 10" for the same product); each other document that uses
    this mixin lets the user pick which one applies to a given line.

## Choosing the right dependency type

- **Dependent** - entering either quantity on a document line recomputes
  the other through the factor, in both directions. Good for a fixed,
  reliable packaging ratio (a box always has 12 units).
- **Independent** - the two quantities never influence each other.
  Good for a secondary quantity that is purely informational (hours of
  work behind a fixed "1 package" sale).
- **Secondary unit priority** - the secondary quantity pre-fills the
  primary one via the factor when a line is first created (or when the
  secondary quantity/unit changes), but once the primary quantity has
  been entered or measured on its own, editing it never overwrites the
  secondary quantity, and the secondary quantity is never silently
  recomputed from a later primary-quantity change either. Good for a
  count that must stay exact (pieces) alongside a primary quantity that
  is only ever an estimate (weight).

## For module developers

To make another model participate in secondary units (compute a quantity
field from a `secondary_uom_id`/`secondary_uom_qty` pair the same way this
module's own product records do), inherit `product.secondary.unit.mixin`
and declare `_secondary_unit_fields = {"qty_field": "<your quantity
field>", "uom_field": "<your UoM field>"}` on your model, then:

- Make `qty_field` a stored, `readonly=False` compute depending on
  `secondary_uom_id`/`secondary_uom_qty`, whose body just calls
  `self._compute_helper_target_field_qty()`.
- Add an `onchange` on your UoM field that calls
  `self._onchange_helper_product_uom_for_secondary()`, so switching the
  primary UoM keeps the secondary quantity consistent for "Dependent"
  lines.

See `purchase_order_secondary_unit` (purchase-workflow) or
`stock_secondary_unit` (stock-logistics-warehouse) for real examples,
including how a `dependency_type` of "Independent"/"Secondary unit
priority" needs extra protection at the points where the target model
would otherwise recompute a quantity that must be preserved exactly (e.g.
splitting a line, merging two lines, or a stored compute retriggering a
sibling compute).
