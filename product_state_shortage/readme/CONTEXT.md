**Business Need**

This module addresses the need to manage product states effectively in scenarios where stock shortages occur. It ensures that products marked as in shortage automatically revert to their default state when their available quantity is updated to a positive value.

**Approach**

The module introduces a boolean field `is_shortage` in the `product.state` model. When enabled, a cron will watch for products under this state and trigger a reset of the products state upon detecting a positive available quantity.
