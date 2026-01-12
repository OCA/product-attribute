# Copyright 2019 Tecnativa - Pedro M. Baeza
# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class ProductCustomerInfo(models.Model):
    _inherit = "product.supplierinfo"
    _name = "product.customerinfo"
    _description = "Customer Pricelist"

    partner_id = fields.Many2one(string="Customer", help="Customer of this product")
    product_name = fields.Char(string="Customer Product Name")
    product_code = fields.Char(string="Customer Product Code")
    # Override fields with corrected help texts
    min_qty = fields.Float(
        help="The minimum quantity to purchase for this customer to benefit from the "
        "price. Expressed in the customer's Product Unit of Measure if set, "
        "otherwise in the default Product Unit of Measure."
    )
    price = fields.Float(help="Price at which the product is sold to this customer.")
    date_start = fields.Date(help="Start date for this customer price")
    date_end = fields.Date(help="End date for this customer price")
    product_uom = fields.Many2one(help="Customer specific unit of measure.")

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Customer Pricelists"),
                "template": "/product_customerinfo/static/xls/"
                "product_customerinfo.xls",
            }
        ]

    @api.model
    def _get_name_search_domain(self, partner_id, operator, name):
        # NOTE: Ideally we could use child_of operator here instead
        # of building top level commercial partner + parent + current contact
        partner = self.env["res.partner"].browse(partner_id)
        partner_ids = (partner + partner.parent_id + partner.commercial_partner_id).ids

        return [
            ("partner_id", "in", partner_ids),
            "|",
            ("product_code", operator, name),
            ("product_name", operator, name),
        ]
