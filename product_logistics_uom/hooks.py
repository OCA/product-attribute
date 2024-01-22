# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging

from odoo.tools import sql

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):  # pragma: nocover
    """Recompute the volume and weight column on product and template
    by converting the value from the uom defined on the product to the default uom
    """
    if sql.column_exists(cr, "product_template", "volume_uom_id"):
        _logger.info("Recompute volume on product.product")
        # get default m3 uom
        cr.execute(
            """
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'uom' AND name = 'product_uom_cubic_meter'
            """
        )
        m3_uom_id = cr.fetchone()[0]
        # get uom factor
        cr.execute(
            """
            SELECT factor
            FROM uom_uom
            WHERE id = %s
            """,
            (m3_uom_id,),
        )
        m3_uom_factor = cr.fetchone()[0]
        # update volume where volume_uom_id is not null and not m3
        cr.execute(
            """
            UPDATE product_product
            SET volume = product_product.volume / product_uom.factor  * %s
            FROM uom_uom product_uom,
            product_template pt
            WHERE product_uom.id = volume_uom_id
                AND pt.id = product_product.product_tmpl_id
                AND volume_uom_id IS NOT NULL AND pt.volume_uom_id != %s
            """,
            (m3_uom_factor, m3_uom_id),
        )
        _logger.info(f"{cr.rowcount} product_product rows updated")
        # update product_template with 1 product_product
        cr.execute(
            """
            UPDATE product_template
            SET Volume = unique_product.volume
            FROM (
                SELECT product_tmpl_id, volume
                FROM product_product
                WHERE volume is not null
                GROUP BY product_tmpl_id, volume
                HAVING COUNT(*) = 1
            ) unique_product
            WHERE product_template.id = unique_product.product_tmpl_id
            AND product_template.volume_uom_id != %s
            """,
            (m3_uom_id,),
        )
        _logger.info(f"{cr.rowcount} product_template rows updated")
    if sql.column_exists(cr, "product_template", "weight_uom_id"):
        _logger.info("Recompute weight on product.product")
        # get default kg uom
        cr.execute(
            """
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'uom' AND name = 'product_uom_kgm'
            """
        )
        kg_uom_id = cr.fetchone()[0]
        # get uom factor
        cr.execute(
            """
            SELECT factor
            FROM uom_uom
            WHERE id = %s
            """,
            (kg_uom_id,),
        )
        kg_uom_factor = cr.fetchone()[0]
        # update weight where weight_uom_id is not null and not kg
        cr.execute(
            """
            UPDATE product_product
            SET weight = product_product.weight / product_uom.factor  * %s
            FROM uom_uom product_uom, product_template pt
            WHERE product_uom.id = weight_uom_id
                AND pt.id = product_product.product_tmpl_id
                AND weight_uom_id IS NOT NULL AND pt.weight_uom_id != %s
            """,
            (kg_uom_factor, kg_uom_id),
        )
        _logger.info(f"{cr.rowcount} product_product rows updated")
        # update product_template with 1 product_product
        cr.execute(
            """
            UPDATE product_template
            SET weight = unique_product.weight
            FROM (
                SELECT product_tmpl_id, weight
                FROM product_product
                WHERE volume is not null
                GROUP BY product_tmpl_id, weight
                HAVING COUNT(*) = 1
            ) unique_product
            WHERE product_template.id = unique_product.product_tmpl_id
            AND product_template.weight_uom_id != %s
            """,
            (kg_uom_id,),
        )
        _logger.info(f"{cr.rowcount} product_template rows updated")
