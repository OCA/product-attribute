# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # Up to 19.0 the template net weight was only computed for single-variant
    # templates. Set it on multi-variant ones when all their variants agree.
    cr.execute(
        """
        UPDATE product_template pt
           SET net_weight = v.net_weight
          FROM (
                SELECT product_tmpl_id, MIN(COALESCE(net_weight, 0)) AS net_weight
                  FROM product_product
                 WHERE active
              GROUP BY product_tmpl_id
                HAVING COUNT(*) > 1
                   AND COUNT(DISTINCT COALESCE(net_weight, 0)) = 1
               ) v
         WHERE pt.id = v.product_tmpl_id
        """
    )
