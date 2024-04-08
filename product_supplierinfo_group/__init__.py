# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from psycopg2.extensions import AsIs

from odoo.tools.sql import (
    create_column,
    create_model_table,
)
from .models.product_supplierinfo import MAPPING_MATCH_GROUP

_schema = logging.getLogger("odoo.schema")

MAPPING_FIELDS_DB = {
    "company_id": "int4",
    "product_tmpl_id": "int4",
    "product_id": "int4",
    "partner_id": "int4",
    "product_name": "varchar",
    "product_code": "varchar",
    "sequence": "int4",
    "unit_price_note": "varchar",
}


def fill_required_group_id_column(cr):
    """
    On installing this module, we have the problem of adding
    on product.supplierinfo:

        group_id = fields.Many2one("product.supplierinfo.group", required=True)

    This is complicated because the product_supplierinfo_group table
    doesn't exist yet:
        - no default value is possible
        - can't put group_id=0 because psycopg/postgres
          enforces constraint that the id exists in DB
        - can't suspend constraints without superuser privileges
        - we want to keep it required=True
        - we don't want to install module twice (once where the constraint
          required can't be applied at the DB layer, once where it can)

    Thus, we must jump through the hoops:
        - Create the table product_supplierinfo_group
        - Populate the table with the right values
        - Fill the newly required group_id on product_supplierinfo
    """
    cr.execute(
        "SELECT count(id) FROM %s",
        (AsIs("product_supplierinfo"),),
    )
    res = cr.fetchall()
    if not res[0][0]:
        # No need to run the hook as they is not data to migrate
        return
    # Create table
    create_model_table(cr, "product_supplierinfo_group")
    for col_name, col_type in MAPPING_FIELDS_DB.items():
        create_column(cr, "product_supplierinfo_group", col_name, col_type)

    # Get grouped values to create supplierinfo groups
    fields_supplierinfo = ",".join(MAPPING_MATCH_GROUP.keys())
    fields_supplierinfo_group = ",".join(MAPPING_MATCH_GROUP.values())
    cr.execute(
        "SELECT %s FROM product_supplierinfo GROUP BY %s",
        (AsIs(fields_supplierinfo), AsIs(fields_supplierinfo)),
    )
    supplierinfo_group_vals = cr.dictfetchall()
    rows = tuple([tuple(row.values()) for row in supplierinfo_group_vals])
    args_str = ",".join(
        cr.mogrify(f"({(len(x)*'%s,')[:-1]})", x).decode("utf-8") for x in rows
    )
    # Populate supplierinfo_group table
    cr.execute(
        "INSERT INTO product_supplierinfo_group(%s) VALUES %s",
        (AsIs(fields_supplierinfo_group), AsIs(args_str)),
    )

    # Update supplierinfo table
    create_column(cr, "product_supplierinfo", "group_id", "int4")

    # Assign the right group to supplierinfo's
    conditions = " AND ".join(
        [
            "p.{} IS NOT DISTINCT FROM g.{}".format(field_supinfo, field_supinfo_group)
            for field_supinfo, field_supinfo_group in MAPPING_MATCH_GROUP.items()
        ]
    )
    cr.execute(
        "UPDATE product_supplierinfo p "
        "SET group_id = g.id "
        "FROM product_supplierinfo_group g "
        "WHERE %s",
        (AsIs(conditions),),
    )
