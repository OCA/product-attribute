# Copyright 2019 Tecnativa - Pedro M. Baeza
# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class ProductCustomerInfo(models.Model):
    _inherit = "product.supplierinfo"
    _name = "product.customerinfo"
    _description = "Customer Pricelist"

    name = fields.Many2one(string="Customer", help="Customer of this product")

    def onchange(self, values, field_name, field_onchange):
        if "product_tmpl_id" in values and field_name != "product_tmpl_id":
            values.pop(
                "product_tmpl_id", None
            )  # otherwise it will be removed from the defaults
        return super(ProductCustomerInfo, self).onchange(
            values, field_name, field_onchange
        )

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Customer Pricelists"),
                "template": "/product_supplierinfo_for_customer/static/xls/"
                "product_customerinfo.xls",
            }
        ]
