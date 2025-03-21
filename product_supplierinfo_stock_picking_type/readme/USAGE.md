1.  Go to *Inventory \> Configuration \> Operations types* and create
    two records named 'Incoming A' and 'Incoming B' with 'Type of
    Operation' equal to 'Receipt'.
2.  Go to *Inventory \> Products \> Products*, then create a product
    named 'Test product' and set 'Purchase' tab as follows:
3.  \[Vendor line 1\] Vendor: Azure Interior, Picking type: Incoming A,
    Price: 5.
4.  \[Vendor line 2\] Vendor: Azure Interior, Picking type: Incoming B,
    Price: 10.
5.  Then click on 'Save'.

Next steps:

Purchase order flow A: \#. Go to *Purchase \> Orders \> Requests for
Quotation* and create a new order as follows: \#. Vendor: Azure
Interior; Product: Test product; Deliver To: Incoming A (add the user to the Manage Multiple Stock Locations permission group to see this field.) \#. The unit price of the product will be 5.

Purchase order flow B: \#. Go to *Purchase \> Orders \> Requests for
Quotation* and create a new order as follows: \#. Vendor: Azure
Interior; Product: Test product; Deliver To: Incoming B (add the user to the Manage Multiple Stock Locations permission group to see this field.) \#. The unit price of the product will be 10.
