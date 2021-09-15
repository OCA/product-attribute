# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    """Quick populate new product.template field 'uom_measure_type'
    to avoid slowness if this is done by the ORM, in the case of
    installation of this module on a large database.
    """

    cr.execute("""
        ALTER TABLE product_template
        ADD column uom_measure_type character varying;
        """)
    cr.execute("""
        UPDATE product_template
        SET uom_measure_type = uom_uom.measure_type
        FROM uom_uom
        WHERE uom_uom.id = product_template.uom_id
        """)
