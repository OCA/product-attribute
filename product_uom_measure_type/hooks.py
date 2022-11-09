# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """Quick populate new product.template field 'uom_measure_type'
    to avoid slowness if this is done by the ORM, in the case of
    installation of this module on a large database.
    """

    _logger.info("Initialize 'measure_type' field on 'uom_category' table")
    cr.execute(
        """
        ALTER TABLE uom_category
        ADD column measure_type character varying;
        """
    )

    uom_datas = [
        ("product_uom_categ_unit", "unit"),
        ("product_uom_categ_kgm", "weight"),
        ("uom_categ_wtime", "working_time"),
        ("uom_categ_length", "length"),
        ("uom_categ_surface", "surface"),
        ("product_uom_categ_vol", "volume"),
    ]

    for (name, measure_type) in uom_datas:
        cr.execute(
            """
            UPDATE uom_category
            SET measure_type = %s
            FROM ir_model_data
            WHERE ir_model_data.res_id = uom_category.id
            AND ir_model_data.module = 'uom'
            AND ir_model_data.name = %s
            """,
            (
                measure_type,
                name,
            ),
        )

    _logger.info("Initialize 'measure_type' field on 'uom_uom' table")
    cr.execute(
        """
        ALTER TABLE uom_uom
        ADD column measure_type character varying;
        """
    )

    cr.execute(
        """
        UPDATE uom_uom
        SET measure_type = uom_category.measure_type
        FROM uom_category
        WHERE uom_category.id = uom_uom.category_id
        """
    )

    _logger.info("Initialize 'uom_measure_type' field on 'product_template' table")
    cr.execute(
        """
        ALTER TABLE product_template
        ADD column uom_measure_type character varying;
        """
    )

    cr.execute(
        """
        UPDATE product_template
        SET uom_measure_type = uom_uom.measure_type
        FROM uom_uom
        WHERE uom_uom.id = product_template.uom_id
        """
    )
