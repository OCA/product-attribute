from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "product.supplierinfo.import.template",
                "product_supplierinfo_import_template",
                "barcode_header_name",
                "search_header_name",
            ),
        ],
    )
