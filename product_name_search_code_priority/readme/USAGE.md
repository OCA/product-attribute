**Usage**

The module works automatically in the background. When users search for products in any Odoo interface (sales orders, purchase orders, etc.):

- **Code Search Priority**: If the search term matches any product's internal reference (default_code), those results are returned immediately
- **Fallback Search**: If no code matches are found, the system falls back to the standard Odoo search behavior (name, barcode, etc.)
- **Improved Accuracy**: Users searching by internal reference get precise results without noise from barcode matches

**Example Scenario:**

*Before the module:*
- User searches for "00030"
- Gets 50+ results including products with barcodes like "1230003051", "1230003062", etc.
- Difficult to find the exact product

*After the module:*
- User searches for "00030" 
- Gets only the product with internal reference "00030"
- Clean, precise results
