This module improves retrieving products when a language is installed and configured.
The default behaviour is to order products by name, which in this case would be slow
because Odoo will process the product's name to translate it.

Warning: This changes the way products are ordered
product are ordered "default_code, id"
instead of "default_code, translated(name), id"

Because Odoo needs the following query to get a translated(name)

.. code-block::

    SELECT "product_product".id
    FROM   "product_product"
    LEFT JOIN "product_template" AS "product_product__product_tmpl_id"
        ON ( "product_product"."product_tmpl_id" =
            "product_product__product_tmpl_id"."id" )
    LEFT JOIN (SELECT res_id,
                        value
                FROM   "ir_translation"
                WHERE  type = 'model'
                        AND name = 'product.template,name'
                        AND lang = 'es_MX'
                        AND value != '') AS
                "product_product__product_tmpl_id__name"
        ON ( "product_product__product_tmpl_id"."id" =
                        "product_product__product_tmpl_id__name"."res_id" )
    WHERE  ( "product_product"."active" = true )
    ORDER  BY "product_product"."default_code",
            Coalesce("product_product__product_tmpl_id__name"."value",
            "product_product__product_tmpl_id"."name"),
            "product_product"."id"
    LIMIT  10


Using a production database executing this query the result is:
 - Planning Time: 1.088 ms
 - Execution Time: 1027.282 ms
 - Total Time: 1028.37 ms

It is so slow.

Using the new order: "default_code, id" the following query is executed now:

.. code-block::

    SELECT "product_product".id
    FROM   "product_product"
    WHERE  ( "product_product"."active" = true )
    ORDER  BY "product_product"."default_code"
    LIMIT  10

The new result is:
 - Planning Time: 0.095 ms
 - Execution Time: 0.529 ms
 - Total Time: 0.624 ms

It is 1.65k times faster

It is because the field ``name`` has the parameter ``translate=True``

So, It will process the original value to translate it

Then, It will order by a column computed on-the-fly of other tables

default_code is a column indexed so the result is faster

Opening the ``/shop`` page could consume 7.5s instead of 1.2s without this module

Odoo is using the _order parameter even if you don't need it.
 - ``products.search(...).write(...)``
 - ``browse().*2many_product_ids.ids``


More info about this on:

  https://github.com/odoo/odoo/pull/61618
