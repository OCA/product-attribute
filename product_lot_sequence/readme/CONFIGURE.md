## Lot Sequence policy

There are two ways you can configure this module through the use of
System Parameter \`product_lot_sequence.policy\`:

- "product": This is the default behaviour once you install this module.
  It's the same than in previous Odoo versions with this module
  installed, i.e. it allows to define a dedicated sequence on each
  product.
- "global": This was the default behaviour from previous Odoo versions
  when this module was not installed, i.e it will always use the same
  global sequence for every product.

If any other value is used for this System Parameter, then you will get
the default behaviour from odoo 15.0 which will look for the last lot
number for each product and will increment it.

## Taking the number only when the lot is created

System Parameter \`product_lot_sequence.consume_on_create\`, default
"False".

When "False", the proposed serial number is taken from the sequence as soon
as it is shown. Canceling the form or replacing the value leaves a gap in
the numbering.

When "True", proposing a number reads it, and the sequence is moved
forward only when the lot is created. Mass creation moves the sequence
past the whole batch rather than by a single number.

## Refusing a serial number that already exists

System Parameter \`product_lot_sequence.duplicate_check\`, default "no".

Odoo only enforces that a serial number is unique per product, which is
not enough when one sequence numbers every product.

- "no": not checked, default behavior.
- "check": check uniqueness for everyone.
- "admin": same as check, except for admins same as "no"

## Default Number of Digits for Product Sequence Generation

The default is 7 digits. To change that to something else, go to the
inventory configuration, find "Sequence Number of Digits" and change the
number.
