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
    # Update the product_attribute_value table by splitting the linked_record_ref field
    # into model and res_id based on a comma delimiter for non-null references.
    cr.execute(
        """
        UPDATE product_attribute_value
        SET
            model = split_part(linked_record_ref, ',', 1),
            res_id = CAST(split_part(linked_record_ref, ',', 2) AS INTEGER)
        WHERE linked_record_ref IS NOT NULL;
    """
    )
