# Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# Copyright (C) 2020-Today Akretion (http://www.akretion.com)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSupplierinfoGroup(models.Model):
    _name = "product.supplierinfo.group"
    _description = "Supplierinfo group"

    product_tmpl_id = fields.Many2one("product.template", required=True)
    supplierinfo_ids = fields.One2many("product.supplierinfo", "supplierinfo_group_id")
    product_id = fields.Many2one(
        "product.product",
        "Product Variant",
        help="If not set, the vendor price will apply to all "
        "variants of this product.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Vendor",
        domain=[("supplier", "=", True)],
        ondelete="cascade",
        required=True,
        help="Vendor of this product",
    )
    product_name = fields.Char(
        "Vendor Product Name",
        help="This vendor's product name will be used when printing "
        "a request for quotation. Keep empty to use the internal one.",
    )
    product_code = fields.Char(
        "Vendor Product Code",
        help="This vendor's product code will be used when printing "
        "a request for quotation. Keep empty to use the internal one.",
    )
    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Assigns the priority to the list of product vendor.",
    )
    unit_price_note = fields.Char(compute="_compute_unit_price_note", store=True)

    @api.depends("supplierinfo_ids")
    def _compute_unit_price_note(self):
        for rec in self:
            if len(rec.supplierinfo_ids) == 0:
                rec.unit_price_note = "-"
            else:
                txt = ""
                uom_precision = rec.product_tmpl_id.uom_id.rounding
                sorted_prices = rec.supplierinfo_ids.sorted(key=lambda r: r.min_qty)
                nbr_prices = len(sorted_prices.ids)
                for idx in range(nbr_prices):
                    curr = sorted_prices[idx]
                    if idx + 1 != nbr_prices:
                        next = sorted_prices[idx + 1]
                        txt += "{} - {} : {}\n".format(
                            curr.min_qty, next.min_qty - uom_precision, curr.price
                        )
                    else:
                        txt += ">= {} : {}".format(curr.min_qty, curr.price)
                rec.unit_price_note = txt
