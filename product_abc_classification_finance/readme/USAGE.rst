To use this module, you need to:

#. Go to Sales or Inventory menu, then to
   Configuration > Products > ABC Classification Profile and create a profile
   with levels. The sum of all levels in the profile should equal 100 and all
   levels must be unique.

#. Assign the profile to product variants. The cron job will automatically
   classify these products into one of the profile's levels based on the total
   cost and total sales of delivered products.
