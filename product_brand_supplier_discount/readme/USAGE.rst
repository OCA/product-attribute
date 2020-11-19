To use this module, you need to:

* Edit a product.brand instance and set a discount to apply for a supplier.
* You may be interested to keep registered discounts
previous to this module installation if so, you can execute this query:
UPDATE product_supplierinfo SET fixed_discount = discount;
