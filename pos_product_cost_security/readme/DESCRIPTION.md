This is a glue module to avoid permission errors when loading data in
the Point of Sale if the user has no `standard_price` (cost) field
permissions.
It also hides the margin and cost fields in Pos Orders and Pos Sale Report
for non-allowed users
