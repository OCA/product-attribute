To use this module, you need to:

#. Go to the product page.
#. In the general tab, there's a list called *Other Prices*.
#. You can add one for every price name available.

To base pricelist rules on that fields, in the pricelist:

#. Add a rule and choose *formula* as the computing method.
#. In the *Based on* dropdown list, select *Other Price*.
#. A new list appear: *Other Price Name*. Pick the one you need.
#. Configure the formula.
#. Now the rule is based on that price for the products that have it
   configured. Otherwise, it will return 0.
