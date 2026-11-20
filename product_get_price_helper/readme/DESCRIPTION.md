Adds a helper function \_get_price() on product.product to compute the
product price based on pricelist, fiscal position, company and date.

The method returns a dict such as:

``` python
{
    "value": 600.0,
    "tax_included": True,
    "discount": 20.0,
    "original_value": 750.0,
}
```
