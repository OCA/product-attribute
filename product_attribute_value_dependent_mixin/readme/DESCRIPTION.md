This technical module introduces a reusable mixin designed to enable any
model to establish dependencies on specific product attribute values. By
inheriting from this mixin, developers can easily link business rules,
configurations, or records to precise product variants without
duplicating complex filtering logic.

- Automatically computes available products and attribute values based
  on the selected product.template.
- Supports domain construction to filter attribute values based on
  context.
- Matching Logic: Includes a is_matching_product(product) method to
  validate whether a specific product variant satisfies the configured
  attribute constraints.
