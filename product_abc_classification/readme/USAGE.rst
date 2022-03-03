To use this module, you need to:

#. Go to Sales or Inventory menu, then to Configuration/Products/ABC Classification Profile
and create a profile with levels. If the classification type is "Percentage" you have to
know that the sum of all levels in the profile should sum 100 and all the levels should
be different.

#. Later you should go to product categories or product variants, and assign them a profile.
Then the cron classification will proceed to assign to these products one of the profile's levels.

NOTE: If you profile (or unprofile) a product category, then all its
child categories and products will be profiled (or unprofiled).
