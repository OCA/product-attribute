To use this module, you need to:

1.  Go to *Sales \> Products \> Pricelists* and create a new Price List.
2.  Add a Pricelist Items to that Price List. Set 'Fixed Price' value on
    the field 'Price type' and set a fixed price.
3.  Go to the new menu *Sales \> Products \> Pricelist Items*, select
    the previously created item and click on the *Revise Prices* button
    (also available in *Action \> Revise Prices*).
4.  In the wizard set 'Date Start', set 'Date End' and set 'Variation %'
    to a value different from 100.
5.  Click on 'Apply' and you will see a new Price List Item that is a
    copy of the previous item. In that new Item the value of the 'Fixed
    Price' field will be the previous price plus that price multiplied
    by the variation percentage and the value of the 'Variation %' will
    contain that value.

To revise (index) all the prices of a pricelist at once:

1.  Open the pricelist in *Sales \> Products \> Pricelists* and click on
    the *Revise Prices* button in the header.
2.  Optionally set a 'Product Category' to only revise the items of
    products in that category (child categories included).
3.  Set 'Date Start', optionally 'Date End', and the 'Variation %', then
    click on 'Apply'.
4.  Every fixed price item of the pricelist that is still valid at the
    start date gets a new revised item; the original items end one
    second before the start date. Items that are not fixed price, that
    already ended or that start later are left untouched.

Items that are not fixed price are never revised; when such items are
selected, they are skipped and a warning is shown.
