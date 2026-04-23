To configure this module, you need to:

1. Navigate to the **Inventory** module.
2. Go to **Sales > Configuration > Products > Product States**.
3. Create or edit a product state and enable the **Is Shortage State** checkbox.
4. Save the changes.

This configuration ensures that products in the specified state will be watched by a cron to automatically revert to the default state when their available quantity becomes positive.
