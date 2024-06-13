This module by itself contains no business logic, but its configuration can be used to
create endpoints' code snippets.

For example:

.. code-block:: python

    prod_data = []
    prod_domain = endpoint.product_assorment_id._get_eval_domain()
    for product in env["product.product"].search(prod_domain):
        data = {"id": product.id, "name": product.display_name}
        if endpoint.include_prices:
            data["price"] = product.list_price
        prod_data.append(data)
    resp = Response(json.dumps(prod_data), content_type="application/json", status=200)
    result = dict(response=resp)
