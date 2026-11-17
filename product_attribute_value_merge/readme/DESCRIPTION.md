Merge attribute values that are the same one, such as "3-4kg" and "3/4kg" created by
different users, without touching the variants that use them, and undo the merge if it
was a mistake.

Since Odoo 18.0 nothing stops two values of an attribute from having the same name, and
deleting a value that archived variants use only archives it, so duplicates appear
easily. This module finds them and merges them:

- The product attribute values of the templates keep their id and only point to the kept
  value, so variants, their combinations and everything hanging from them (stock, sales,
  accounting) stay as they are.
- Every other stored reference to the merged values (for example a lot keeping the
  fishing area of its product) is moved to the kept value.
- The merged values are archived, not deleted, and every moved record is logged. Undoing
  the merge puts back the records that still hold the kept value; records created or
  changed after the merge keep their current value.
- The name of the kept value is chosen per language, filling the languages it lacks with
  the names of the merged values.
