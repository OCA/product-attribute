## Product Class

This module introduces **Product Classes** for standardizing product setup and attribute management. It allows you to:

1. **Define Product Classes** — Group related products into classes (e.g., "Furniture", "Electronics")
2. **Constrain Attributes per Class** — Specify which attributes are allowed for each class
3. **Mark Required Attributes** — Designate certain attributes as mandatory for products in that class
4. **Enforce Validation** — Prevent products from using attributes outside their class or missing required attributes

### Key Features

- **Bridge Model (`product.class.attribute.line`)** — Manages the relationship between classes and attributes, storing both allowed attributes and a `required` flag
- **Strict Validation** — Products assigned to a class must:
  - Use only attributes defined in that class
  - Provide values for all required attributes
- **UI Enforcement** — Attribute selection in product forms is restricted by the class domain filter
- **Management Views** — Full CRUD interface for product classes (Inventory > Configuration > Product Classes, Sales > Configuration > Product Classes)

### Technical Architecture

- `product.class` — Main product classification model
- `product.class.attribute.line` — Bridge model linking classes to attributes with a `required` flag
- `product.attribute` (inherited) — Extended with reverse one-to-many to track which classes use it
- `product.template` (inherited) — Added class validation and computed required-attribute tracking
