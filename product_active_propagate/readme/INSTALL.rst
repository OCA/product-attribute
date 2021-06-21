If you are installing this module on a database with existing data, you could want
to execute the two following SQL requests, to fix some inconsistent data.


* Disable templates that do not have a single variant active

.. code-block:: sql

    UPDATE product_template pt
    SET active = false
    WHERE id in (
        SELECT pt.id
        FROM product_template pt
        INNER JOIN product_product pp on pp.product_tmpl_id = pt.id
        WHERE pt.active = true
        GROUP BY pt.id
        HAVING sum((pp.active)::int) = 0
    );


* Enable templates that have at least one active variant

.. code-block:: sql

    UPDATE product_template pt
    SET active = true
    WHERE id in (
        SELECT pt.id
        FROM product_template pt
        INNER JOIN product_product pp on pp.product_tmpl_id = pt.id
        WHERE pt.active = false
        GROUP BY pt.id
        HAVING sum((pp.active)::int) != 0
    );
