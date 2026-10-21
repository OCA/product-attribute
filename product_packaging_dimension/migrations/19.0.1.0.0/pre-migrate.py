# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.tools import sql


# ``product_logistics_uom`` is optional in 19.0, but some 18.0 databases may
# have used its arbitrary default UoM parameters. Keep reading those values
# during migration so their existing packaging dimensions and weights are
# converted to the same configured target UoMs before the legacy per-record
# UoM columns disappear.
def _get_uom_from_param(env, param, fallback_xmlid):
    """Return an optional configured target UoM, falling back to UoM defaults."""
    uom_id = env["ir.config_parameter"].sudo().get_param(param)
    if uom_id:
        return env["uom.uom"].browse(int(uom_id))
    return env.ref(fallback_xmlid)


def _get_target_length_uom(env):
    """Return the target length UoM from optional params or UoM defaults."""
    fallback_xmlid = "uom.product_uom_millimeter"
    if (
        env["ir.config_parameter"].sudo().get_param("product.volume_in_cubic_feet")
        == "1"
    ):
        fallback_xmlid = "uom.product_uom_foot"
    return _get_uom_from_param(env, "product_default_length_uom_id", fallback_xmlid)


def _get_target_weight_uom(env):
    """Return the target weight UoM from optional params or UoM defaults."""
    fallback_xmlid = "uom.product_uom_kgm"
    if env["ir.config_parameter"].sudo().get_param("product.weight_in_lbs") == "1":
        fallback_xmlid = "uom.product_uom_lb"
    return _get_uom_from_param(env, "product_default_weight_uom_id", fallback_xmlid)


def _convert_dimensions_to_target_length_uom(env):
    """Keep dimension values unchanged semantically after dropping length_uom_id.

    In 18.0, each packaging could store its own ``length_uom_id``.
    In 19.0, packaging dimensions use the product length UoM helper.
    Before the ORM removes the old column, convert stored length/width/height
    numbers to the configured target UoM so existing packaging dimensions still
    mean the same physical size after the upgrade.
    """
    if not sql.column_exists(env.cr, "product_packaging", "length_uom_id"):
        return
    target_uom = _get_target_length_uom(env)
    # Equivalent to old_uom._compute_quantity(value, target_uom, round=False).
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_packaging packaging
           SET packaging_length =
                   packaging.packaging_length * old_uom.factor / %s,
               height = packaging.height * old_uom.factor / %s,
               width = packaging.width * old_uom.factor / %s
          FROM uom_uom old_uom
         WHERE old_uom.id = packaging.length_uom_id
           AND packaging.length_uom_id IS NOT NULL
           AND packaging.length_uom_id != %s
        """,
        (
            target_uom.factor,
            target_uom.factor,
            target_uom.factor,
            target_uom.id,
        ),
    )


def _convert_weight_to_target_weight_uom(env):
    """Keep packaging weights unchanged semantically after dropping weight_uom_id.

    The 19.0 ``product_packaging`` module owns ``weight`` on product packaging,
    and the product weight UoM helper supplies the target configured UoM.
    Convert legacy per-record weight values before ``weight_uom_id`` disappears.
    """
    if not sql.column_exists(env.cr, "product_packaging", "weight_uom_id"):
        return
    target_uom = _get_target_weight_uom(env)
    # Equivalent to old_uom._compute_quantity(value, target_uom, round=False).
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_packaging packaging
           SET weight = packaging.weight * old_uom.factor / %s
          FROM uom_uom old_uom
         WHERE old_uom.id = packaging.weight_uom_id
           AND packaging.weight_uom_id IS NOT NULL
           AND packaging.weight_uom_id != %s
        """,
        (
            target_uom.factor,
            target_uom.id,
        ),
    )


@openupgrade.migrate()
def migrate(env, version):
    """Normalize legacy per-record UoM values before model initialization."""
    if not sql.table_exists(env.cr, "product_packaging"):
        return
    _convert_dimensions_to_target_length_uom(env)
    _convert_weight_to_target_weight_uom(env)
