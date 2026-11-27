This module extends the product name search functionality to prioritize exact matches on the internal reference (default_code) field. When searching for products, the system first tries to find matches by internal reference before falling back to the standard search behavior.

In databases with many products that have barcodes, the quick search results can become polluted with an excessive number of false positive matches. This is especially problematic when:

* You have thousands of products with similar barcode patterns
* Typing internal references (like "00030") returns many unrelated products whose barcodes contain similar number sequences
* Users frequently search by internal reference but get overwhelmed by barcode matches
* The search performance is degraded by processing too many irrelevant results
