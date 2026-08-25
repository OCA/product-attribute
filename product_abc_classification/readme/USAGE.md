To use this module, you need to:

1.  Go to Inventory menu, then to Configuration/Products/ABC
    Classification Profile and create a profile with its levels. Each level says how big a share of your catalogue it should cover (% Products) and how big a share of your business it should represent (% Indicator). Both columns should sum 100, and the % Indicator of every level should be different, since that is what ranks them.

    For example, a profile with three levels:

    | Name | % Products | % Indicator |
    |------|------------|-------------|
    | A    | 20         | 80          |
    | B    | 30         | 15          |
    | C    | 50         | 5           |

    That reads as "20% of my products should account for 80% of my business, another 30% of them for 15% of it, and the remaining 50% for just 5%". A is the top level because it has the highest % Indicator, so the few products that end up in A are the ones to watch first.

2.  Later you should go to product categories or product variants, and assign them a profile. Then the cron classification will pick up these products and give them a level.

3.  Go to Inventory/Products/Products ABC Classification to review the result, and change the level of a product by hand when you disagree with it.

NOTE: with the standard Manual profile the cron does not work out which level a product belongs to. It simply gives every product it picks up the highest level, and leaves the already classified products untouched. Other modules extending this one allow to select other non-manual classification

NOTE: applying a profile from a product category affects the products directly in that category, and replaces the profiles they already had.
