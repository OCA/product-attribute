# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Fetch records with temp_model and temp_res_id filled
    cr.execute(
        """
        SELECT id, temp_model, temp_res_id
        FROM product_attribute_value
        WHERE temp_model IS NOT NULL AND temp_res_id IS NOT NULL
    """
    )
    records = cr.fetchall()

    # Loop through each record to update the 'model' and 'res_id' fields
    for rec_id, temp_model, temp_res_id in records:
        # Directly update 'model' and 'res_id' fields in product_attribute_value
        cr.execute(
            """
            UPDATE product_attribute_value
            SET model = %s, res_id = %s
            WHERE id = %s
        """,
            [temp_model, temp_res_id, rec_id],
        )

    # Remove the temporary columns after migration
    cr.execute(
        """
        ALTER TABLE product_attribute_value
        DROP COLUMN temp_model,
        DROP COLUMN temp_res_id
    """
    )
