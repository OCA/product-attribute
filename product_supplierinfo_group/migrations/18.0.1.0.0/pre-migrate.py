from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Rename view xml ids."""
    xml_spec = [
        (
            "product_supplier_info_group.supplierinfo_group_view_tree",
            "product_supplier_info_group.supplierinfo_group_view_list",
        ),
        (
            "product_supplier_info_group.product_template_tree_view",
            "product_supplier_info_group.product_template_form_view",
        ),
    ]
    openupgrade.rename_xmlids(env.cr, xml_spec)
