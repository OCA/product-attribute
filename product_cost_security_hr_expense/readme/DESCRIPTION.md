Make `product_cost_security` and `hr_expense` compatible.

In the expense product form, the unit-of-measure span after the cost field
uses `standard_price` in its `invisible` expression. `product_cost_security`
restricts `standard_price` to the *Product costs / Read* group, while that span
was shown to every internal user. Odoo then reports an *Access Rights
Inconsistency* warning when loading the view.

This glue module restricts the span to the same group, so the view is
consistent and the warning disappears.
