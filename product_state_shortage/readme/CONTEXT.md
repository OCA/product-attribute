**Business Need**

This module addresses the need to manage product states effectively in scenarios where stock shortages occur. It ensures that products marked as in shortage automatically revert to their default state when new stock is received.

**Approach**

The module introduces a boolean field `is_shortage` in the `product.state` model. When enabled, it triggers a reset of the product state upon stock receipt validation.
