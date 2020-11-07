# Copyright 2020 Forgeflow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
    UPDATE product_product as pp
    SET
        manufacturer = pt.manufacturer,
        manufacturer_pname = pt.manufacturer_pname,
        manufacturer_pref = pt.manufacturer_pref,
        manufacturer_purl = pt.manufacturer_purl
    FROM product_template AS pt
    WHERE
        (pt.manufacturer IS NOT NULL
        OR pt.manufacturer_pname != ''
        OR pt.manufacturer_pref != ''
        OR pt.manufacturer_purl != '')
        AND pt.id = pp.product_tmpl_id
        """
    )
