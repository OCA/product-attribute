- Company dependent fields pointing to attribute values are not moved; the wizard warns
  how many records hold the merged values there.
- A record that gets a merged value in a transaction committed while the merge runs
  (after it started, before it locks the values) keeps the archived value.
- Values referenced by id in saved filters, default values or server actions keep
  pointing to the merged value.
- Generic references (`fields.Reference`, `res_model`/`res_id`) to attribute values are
  not moved.
- A product having two of the values on the same attribute line is left as it is:
  merging those variants would mean merging products.
