from openupgradelib import openupgrade

xml_ids = ["product_template_tags.product_template_tag_form_view",
           "product_template_tags.product_template_tag_search_view",
           "product_template_tags.product_template_tag_tree_view",
           "product_template_tags.product_template_tag_act_window",
           "product_template_tags.product_template_form_view",
           "product_template_tags.product_template_kanban_view",
           "product_template_tags.product_template_search_view",
           "product_template_tags.product_template_tree_view",
           "product_template_tags.product_kanban_view",
           "product_template_tags.product_product_tree_view",
           ]

@openupgrade.migrate()
def migrate(env, version):
    # Remove the unused xml views.
    openupgrade.delete_records_safely_by_xml_id(env, xml_ids)
    # Copy the product template and tag ids fields to the new relation table.
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO product_tag_product_template_rel(product_template_id, product_tag_id)
        SELECT product_tmpl_id, tag_id FROM product_template_product_tag_rel
        """,
    )
    