from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Update multi-company rule for supplierinfo groups."""
    env.ref(
        "product_supplier_info_group.product_supplierinfo_group_multi_company_rule"
    ).domain_force = "[('company_id', 'in', company_ids + [False])]"
