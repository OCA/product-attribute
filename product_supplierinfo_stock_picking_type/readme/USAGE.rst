#. Go to *Inventory > Configuration > Operations types* and create two records
   named 'Incoming A' and 'Incoming B' with 'Type of Operation' equal to
   'Receipt'.
#. Go to *Inventory > Products > Products*, then create a product named
   'Test product' and set 'Purchase' tab as follows:
#. [Vendor line 1] Vendor: Azure Interior, Picking type: Incoming A, Price: 5.
#. [Vendor line 2] Vendor: Azure Interior, Picking type: Incoming B, Price: 10.
#. Then click on 'Save'.

Next steps:

Purchase order flow A:
#. Go to *Purchase > Orders > Requests for Quotation* and create a new order as follows:
#. Vendor: Azure Interior; Product: Test product; Deliver To: Incoming A (under 'Other information' tab)
#. The unit price of the product will be 5.

Purchase order flow B:
#. Go to *Purchase > Orders > Requests for Quotation* and create a new order as follows:
#. Vendor: Azure Interior; Product: Test product; Deliver To: Incoming B (under 'Other information' tab)
#. The unit price of the product will be 10.
