To use this module, you need to:

1. Navigate to the **Inventory** module.
2. Go to **Sales > Configuration > Products > Product States** and create a state with the **Is Shortage State** checkbox enabled.
3. Assign the shortage state to products as needed.
4. A cron will watch those products so that when the available quantity of such a product becomes positive, it will automatically revert to the default state.
