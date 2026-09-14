Vendor pricelists sheet files could come in a variety of column formats. We can configure templates to match them to know what data we need to store in our pricelist.

To do so:

1. Go to *Purchase > Configuration > Vendor pricelist import templates*.
2. Edit or create a new one.
3. Create a template name.
4. Assign a default supplier. (Set a default supplier that will be associated with this template)
5. In the **Header Offset**, determine the line where the headers are located. (Specify the line number where the column headers are found in your sheet file)
6. In the **Sheet Number**, we will be able to specify the page number to select it.
7. In the **Search Header Name**, set the name of the column you want to filter by. (Indicate the column name used for filtering the data)
8. In the Search Field, set the data you want to filter by. (Specify the field used for filtering)
9. Set a headers mapping with the rest header names and which fields we should update. (Map the remaining header names to the corresponding fields that should be updated in the system)
10. A header mapping could have no related field, but is important to have it if we want to detect the sheet data when we are importing.
11. The order isn't important. (The order of the header mappings does not affect the import process)
12. If **Only Update Existing** is checked, only existing pricelists will be updated; no new ones will be created.
13. If **Show Not Updated Rates** is enabled, the unupdated rates will be shown grouped at the end of the import.
14. If a column in the sheet is empty, set a field with a space (" ") inside to ensure a match.
