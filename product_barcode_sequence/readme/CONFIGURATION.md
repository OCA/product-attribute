To configure barcode generation for a product category:

1. Go to **Products > Configuration > Product Categories**
2. Select or create a category
3. In the **Barcode Configuration** section:
   * Enable **Auto Generate Barcode**
   * Set a **Barcode Prefix** (1-12 digits)
   * The system will automatically create a barcode sequence

Barcode Format:

* EAN-13 format (13 digits total)
* First digits: Category prefix (configurable)
* Middle digits: Sequential number
* Last digit: GTIN check digit (automatically calculated)

Example:

If a category has prefix "123456":
* First product: 1234560000018
* Second product: 1234560000025
* Third product: 1234560000032

The check digit (last number) is calculated using the GTIN algorithm.
