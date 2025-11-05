# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import csv
import io
from datetime import datetime

from odoo import http
from odoo.http import request


class CatalogExportController(http.Controller):
    @http.route(
        ["/feed/export/products.csv"],
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def export_products_csv(self, **kwargs):
        """
        Export product feed to CSV applying pricelist.
        Params:
          pricelist_id: ID of the pricelist (or user default pricelist)
          fields: comma-separated list of fields
          active: true/false
        """
        fields_param = (
            kwargs.get("fields") or "name,default_code,barcode,list_price,qty_available"
        )
        fields = [f.strip() for f in fields_param.split(",") if f.strip()]
        active = kwargs.get("active", "true").lower() != "false"
        pricelist_id = kwargs.get("pricelist_id")
        pricelist = None
        if pricelist_id:
            pricelist = (
                request.env["product.pricelist"].browse(int(pricelist_id)).exists()
            )
        if not pricelist:
            partner = request.env.user.partner_id
            pricelist = partner.property_product_pricelist
        domain = [("active", "=", active), ("sale_ok", "=", True)]
        products = request.env["product.product"].search(domain)
        buf = io.StringIO()
        writer = csv.writer(buf, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)

        def get_val(rec, field):
            if field == "list_price":
                return (
                    pricelist._get_product_price(rec, 1.0)
                    if pricelist
                    else rec.list_price
                )
            val = rec[field] if field in rec._fields else ""
            if hasattr(val, "name") and val._name != "ir.attachment":
                return val.name
            if hasattr(val, "ids"):
                return ",".join(str(x) for x in val.ids)
            if isinstance(val, datetime):
                return val.isoformat()
            return val if val is not False else ""

        for rec in products:
            writer.writerow([get_val(rec, f) for f in fields])

        csv_bytes = buf.getvalue().encode("utf-8-sig")
        headers = [
            ("Content-Type", "text/csv; charset=utf-8"),
            ("Content-Disposition", 'attachment; filename="products.csv"'),
        ]
        return request.make_response(csv_bytes, headers=headers)
