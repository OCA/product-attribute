Make 'Product Cost Security' and 'Stock account' modules compatible.

Avoids permission errors during the stock valuation layer creation, which
would happen when stock users (with no access to product costs) tried to
perform valid stock-related operations, like creating stock valuation layers.
