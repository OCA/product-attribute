from . import models
from odoo import api, SUPERUSER_ID
from .models.product_supplierinfo import FIELDS_MATCH_GROUP


def fill_required_group_id_column(cr, registry):
    def refresh_supplierinfo_groups(supplierinfos):
        """
        Correct empty required supplierinfo_group_id field
        """
        fields_fmt = ",".join(FIELDS_MATCH_GROUP)
        query = "SELECT {} FROM product_supplierinfo".format(fields_fmt)
        env.cr.execute(query)
        all_vals = env.cr.dictfetchall()
        for idx, rec in enumerate(supplierinfos):
            if rec.supplierinfo_group_id:
                continue
            vals_from_db = all_vals[idx]
            vals = {
                field: vals_from_db[field]
                if type(getattr(rec, field)) == type(set)
                else vals_from_db[field]
                for field in FIELDS_MATCH_GROUP
            }
            group = rec._find_or_create_supplierinfo_group(vals)
            rec.supplierinfo_group_id = group

    env = api.Environment(cr, SUPERUSER_ID, {})
    supplierinfos = env["product.supplierinfo"].search([], order="id asc")
    refresh_supplierinfo_groups(supplierinfos)
