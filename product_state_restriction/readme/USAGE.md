# Usage

## 1. Install

1. Install **Product State** (`product_state`) if it is not already installed.
2. Install this module (**Product State Restrictions**).
3. Optional: install `product_state_sale` if you want the Product States menu under **Sales → Configuration → Products**.

## 2. Configure product states

1. Go to **Sales → Configuration → Products → Product States**  
   (or the equivalent menu under Inventory / Product, depending on installed modules).
2. Open an existing state (for example *Obsolete* or *End of Lifecycle*) or create a new one (for example *On Hold* / *Issue*).
3. In the **Restrictions** section, enable the rules you need:

   | Flag | Effect |
   |------|--------|
   | **Restrict Sales** | Products in this state cannot be sold. `sale_ok` is set to `False` and confirming a sales order that contains the product is blocked. |
   | **Restrict Manufacturing** | Products cannot be manufactured as finished goods and cannot be consumed as components. Blocked when confirming an MO and when clicking **Produce** / **Mark as Done**. |
   | **Restrict Outgoing Moves** | Products cannot leave the warehouse (e.g. customer deliveries). Validation of the corresponding stock move is blocked. |

4. Save the state.

Typical setup examples:

- **sellable (Normal)**: all restrictions off  
- **draft (In Development)**: Restrict Sales (+ optionally Restrict Outgoing)  
- **end / obsolete**: Restrict Sales, Restrict Manufacturing, Restrict Outgoing  
- **custom “Issue / On Hold”**: all three restrictions on until the problem is resolved  

## 3. Assign a state to a product

1. Open a product template.
2. Set the **State** field (status bar / many2one provided by `product_state`).
3. Save.

Effects:

- If the state has **Restrict Sales**, `Can be Sold` (`sale_ok`) is turned off automatically.
- Moving the product back to a non-restricted state turns `sale_ok` back on (unless you changed it manually for other reasons).

You can also change restriction flags on a state that already has products assigned: all those products are updated in batch (for `sale_ok`).

## 4. What users will see

| Action | When restricted |
|--------|------------------|
| Confirm sales order | Error: product is in a restricted state and cannot be sold. |
| Confirm manufacturing order | Error: finished product or a component is restricted for manufacturing. |
| Produce / Mark as Done on MO | Same manufacturing restriction check (so production cannot bypass planning). |
| Validate outgoing transfer / delivery | Error: product cannot leave the warehouse in this state. |

Messages include the product name and the state name so warehouse and sales users can react quickly (change state, remove the line, or escalate).

## 5. Recommended process

1. Define which lifecycle states should block which operations.
2. Train users to move products to *On Hold* / *Issue* (or *Obsolete*) when there is a quality or master-data problem.
3. After the issue is resolved, move the product back to *sellable* (or the appropriate open state).
4. Restrictions are lifted automatically according to the flags on the new state.

## 6. Notes

- Restrictions are **product-level** (via the product’s state), not lot/serial-level. For lot holds, use Quality or a dedicated lot-blocking module.
- `sale_ok = False` hides the product from normal sales selection; the confirm check is an extra safety net.
- Manufacturing is checked both at confirm and at produce time, so users cannot skip the rule by producing without a prior confirm step in atypical flows.