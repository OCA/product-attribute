# Copyright 2021 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    ir_attachment = env["ir.attachment"]

    # Attachments are not removed from the database when the field on the
    # anchor model is removed, but we still need to adapt the contents
    # in ir_attachment so that the widget 'many2many_binary' knows how to
    # find the attachments from the UI.
    for old_field_name, new_table_rel_name in [
        ("conformity_declaration", "product_conformity_declaration_rel"),
        ("ce_certificate_medical_class", "product_ce_certificate_medical_class_rel"),
    ]:
        for attachment in ir_attachment.search(
            [
                ("res_model", "=", "product.template"),
                ("res_field", "=", old_field_name),
            ]
        ):
            env.cr.execute(
                """
                INSERT INTO {}(product_template_id, attachment_id)
                VALUES(%s, %s);
                """.format(
                    new_table_rel_name
                ),
                (attachment.res_id, attachment.id),
            )
            env.cr.execute(
                """
                UPDATE ir_attachment
                SET res_field = NULL,
                    res_id = 0
                WHERE id = %s;
                """,
                (attachment.id,),
            )
