Once the alphabetical sort is enabled on an attribute, simply add or rename
values: their order is updated automatically.

To sort on another field, extend the selection of the sort field in a custom
module:

``` python
class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def _selection_sort_field(self):
        return super()._selection_sort_field() + [("code", self.env._("Code"))]
```
