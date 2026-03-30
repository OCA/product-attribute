from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(
        env.cr, "production_lot_ingredient_value"
    ) and not openupgrade.table_exists(env.cr, "stock_lot_ingredient_value"):
        openupgrade.rename_models(
            env.cr, [("production.lot.ingredient.value", "stock.lot.ingredient.value")]
        )
        openupgrade.rename_tables(
            env.cr, [("production_lot_ingredient_value", "stock_lot_ingredient_value")]
        )
    fields_rename_spec = [
        ("product.product", "product_product", "allergen_id", "allergen_ids"),
        ("product.template", "product_template", "allergen_id", "allergen_ids"),
    ]
    openupgrade.rename_fields(fields_rename_spec)
