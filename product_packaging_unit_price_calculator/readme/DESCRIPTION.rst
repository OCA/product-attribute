This module adds a wizard that allows the user to compute a unit price by
selecting a specific `product.packaging` related to the product and the
price of that package. The computation is done based on the quantity `qty`
of product set on the packaging.

The wizard is accessible via buttons located in a few different places in the UI

* Next to the sale price of the product on the product form
* Next to the price of a product supplier info  form
* Next to the price of price list item in the tree view
* Below the fixed price of a price list item

When the wizard is saved the value of the unit price located next to the button
is updated by the computed unit price of the wizard.

The sale price of a `product.packaging` is displayed in the packaging list on
the Inventory page of the product form.
