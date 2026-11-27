# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    product_standard_price = fields.Float(
        string="Product actual standard price",
        related="product_tmpl_id.standard_price",
    )

    theoritical_standard_price = fields.Monetary(
        string="Theoritical Cost",
        compute="_compute_theoritical_standard_price",
        currency_field="currency_id",
    )

    diff_supplierinfo_product_standard_price = fields.Monetary(
        string="current cost difference",
        currency_field="currency_id",
        compute="_compute_diff_supplierinfo_product_standard_price",
        help="Difference between the cost of this supplierinfo and the cost of the product",
    )

    #
    # Other functions
    #
    def _get_standard_price_fields(self):
        res = [
            "product_uom",
            "currency_id",
            "price",
            "product_tmpl_id.uom_po_id",
            "product_id.uom_po_id",
        ]
        # Make the function compatible when "purchase_discount"
        # or "purchase_triple_discount" are installed
        for field in ["discount", "discount2", "discount3"]:
            if field in self._fields:
                res.append(field)
        return res

    @api.depends(lambda x: x._get_standard_price_fields())
    def _compute_theoritical_standard_price(self):
        for supplierinfo in self:
            uom = (
                supplierinfo.product_uom
                or supplierinfo.product_tmpl_id.uom_po_id
                or supplierinfo.product_id.uom_po_id
            )
            if uom:
                currency = supplierinfo.currency_id
                destination_uom = (
                    supplierinfo.product_tmpl_id.uom_id
                    or supplierinfo.product_id.uom_id
                )
                price = supplierinfo.price
                if "discount" in self._fields:
                    price *= 1 - supplierinfo.discount / 100
                if "discount2" in self._fields:
                    price *= 1 - supplierinfo.discount2 / 100
                if "discount3" in self._fields:
                    price *= 1 - supplierinfo.discount3 / 100
                supplierinfo.theoritical_standard_price = currency.round(
                    uom._compute_price(price, destination_uom)
                )
            else:
                supplierinfo.theoritical_standard_price = False

    @api.depends("theoritical_standard_price", "product_standard_price")
    def _compute_diff_supplierinfo_product_standard_price(self):
        for supplierinfo in self.filtered(lambda x: x.product_tmpl_id):
            supplierinfo.diff_supplierinfo_product_standard_price = (
                supplierinfo.product_standard_price
                - supplierinfo.theoritical_standard_price
            )

    # Functions to change product fields
    def set_product_standard_price_from_supplierinfo(self):
        for supplierinfo in self.filtered(lambda x: x.product_tmpl_id):
            old_product_standard_price = supplierinfo.product_tmpl_id.standard_price
            # Set new standard_price
            supplierinfo.product_tmpl_id.standard_price = (
                supplierinfo.theoritical_standard_price
            )
            diff_percentage = (
                (
                    supplierinfo.product_tmpl_id.standard_price
                    - old_product_standard_price
                )
                / old_product_standard_price
                * 100
                if old_product_standard_price != 0
                else 100
            )
            diff_percentage_str = str(round(diff_percentage, 1)) + "%"
            self.env.user.notify_success(
                message=(_("Price difference : %s") % (diff_percentage_str,)),
                title=(
                    _("New standard price for %s") % supplierinfo.product_tmpl_id.name
                ),
            )
