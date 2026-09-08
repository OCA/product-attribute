## Fields

The mixin exposes the following fields:

- `product_tmpl_id`: the product template to filter on (optional).
- `product_id`: a specific product variant (optional).
- `attribute_value_ids`: a set of attribute values to filter on (optional).
- `available_product_domain`: a computed domain to restrict the selection
  of `product_id` in views, based on `product_tmpl_id`.
- `available_attribute_value_domain`: a computed domain to restrict the
  selection of `attribute_value_ids` in views, based on `product_tmpl_id`.

## Inheriting the Mixin

To use this mixin, inherit from `attribute.value.dependent.mixin` in your
model alongside your base model:

```python
from odoo import fields, models


class MyModel(models.Model):
    _name = "my.model"
    _inherit = ["my.model", "attribute.value.dependent.mixin"]
```

All fields from the mixin (`product_tmpl_id`, `product_id`,
`attribute_value_ids`, `available_product_domain`,
`available_attribute_value_domain`) are automatically available on your
model.

## Using the Domain Fields in a Form View

The computed domain fields must be referenced in the `domain` attribute of
the corresponding fields in the view. Odoo 18.0 automatically loads fields
referenced in `domain` attributes, so no additional declaration is needed.

```xml
<record id="view_my_model_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form>
            <group>
                <field name="product_tmpl_id"/>
                <field name="product_id"
                       domain="available_product_domain"
                       context="{'default_product_tmpl_id': product_tmpl_id}"/>
                <field name="attribute_value_ids"
                       domain="available_attribute_value_domain"
                       widget="many2many_tags"/>
            </group>
        </form>
    </field>
</record>
```

## Matching Logic

The `is_matching_product(product)` method validates whether a given product
variant satisfies the configured constraints. All fields are optional and
act as independent filters combined with AND logic:

- If `product_id` is set, it is the most restrictive criterion: the method
  returns `True` only if the given product is exactly that variant,
  regardless of other fields.
- If `product_tmpl_id` is set, the given product must belong to that
  template.
- If `attribute_value_ids` is set, the given product must match the
  configured attribute values with the following logic:
  - Values belonging to the **same attribute** are combined with **OR**
    (e.g. size S *or* M).
  - Values belonging to **different attributes** are combined with **AND**
    (e.g. size S or M *and* color Red).
  - Since an attribute value can exist across multiple templates,
    `product_tmpl_id` and `attribute_value_ids` should be used together
    to avoid unintended matches across templates.
- If no field is set, the method returns `True` for any product (no
  constraint).

## Using `is_matching_product`

The `is_matching_product(product)` method can be called from Python code
to check whether a given `product.product` record satisfies the constraints
defined on a mixin record:

```python
for rule in self.env["my.model"].search([]):
    if rule.is_matching_product(product):
        # apply rule
```
