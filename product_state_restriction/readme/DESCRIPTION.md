# Product State Restrictions

This module extends the OCA **Product State** lifecycle with configurable operational restrictions.

It builds on the standard product states. On each state you can define whether products in that state are allowed to be sold, manufactured, or moved out of the warehouse. When a product is assigned to a restricted state (or when the restriction flags on a state are changed), the system enforces the rules automatically.

## Features

- **Restrict Sales**: products cannot be sold; `sale_ok` is kept in sync and sales order confirmation is blocked.
- **Restrict Manufacturing**: finished products and components cannot be used in manufacturing (blocked on MO confirm and on Produce / Mark as Done).
- **Restrict Outgoing Moves**: products cannot leave the warehouse (customer deliveries and other outgoing stock moves are blocked).

## Why this module

`product_state` only provides the lifecycle field. It does not lock sales, manufacturing, or inventory flows. This module adds the missing operational control in a modular, upgrade-safe way, using official extension points (for example the `_inverse_product_state_id` hook) instead of patching core code.

## Dependencies

- `product_state` (OCA)
- `sale` (for sales restrictions)
- `mrp` (for manufacturing restrictions)
- `stock` (for outgoing move restrictions)

## Technical notes

- Restriction flags live on `product.state`.
- Changing a product’s state updates `sale_ok` via the inverse method on `product.template`.
- Changing `restrict_sale` on a state updates `sale_ok` on all products currently in that state.
- Hard checks run on:
  - `sale.order` → `action_confirm`
  - `mrp.production` → `action_confirm` and `button_mark_done`
  - `stock.move` → `_action_done` (outgoing destinations)

This keeps behaviour consistent whether the user works from the UI, imports, or automated flows.