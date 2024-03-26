# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Add new columns (model and res_id) to the table
    cr.execute(
        """
        ALTER TABLE product_attribute_value
        ADD COLUMN IF NOT EXISTS model VARCHAR,
        ADD COLUMN IF NOT EXISTS res_id INTEGER
    """
    )
    # Extract and store model name and res ID from the linked_record_ref field
    cr.execute(
        """
        SELECT id, linked_record_ref
        FROM product_attribute_value
        WHERE linked_record_ref IS NOT NULL
    """
    )
    for rec_id, linked_ref in cr.fetchall():
        if linked_ref:
            model_name, res_id = linked_ref.split(",")
            # Update the new columns with extracted data
            cr.execute(
                """
                UPDATE product_attribute_value
                SET model = %s, res_id = %s
                WHERE id = %s
            """,
                (model_name, res_id, rec_id),
            )
