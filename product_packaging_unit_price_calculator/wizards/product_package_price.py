# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductPackagePrice(models.TransientModel):
    _name = "product.package.price.wizard"
    _description = "Wizard to compute unit price from packaging price"

    def _default_product_tmpl_id(self):
        return self.env["product.template"].browse(self._context.get("product_tmpl_id"))

    def _default_product_pricelist_item_id(self):
        if self._context.get("active_model") != "product.pricelist.item":
            return False
        return self.env["product.pricelist.item"].browse(self._context.get("active_id"))

    def _default_product_supplierinfo_id(self):
        if self._context.get("active_model") != "product.supplierinfo":
            return False
        return self.env["product.supplierinfo"].browse(self._context.get("active_id"))

    def _default_product_id(self):
        if self._context.get("active_model") != "product.product":
            return False
        return self.env["product.product"].browse(self._context.get("active_id"))

    product_tmpl_id = fields.Many2one(
        "product.template", default=lambda self: self._default_product_tmpl_id()
    )
    product_id = fields.Many2one(
        "product.product", default=lambda self: self._default_product_id()
    )
    product_pricelist_item_id = fields.Many2one(
        "product.pricelist.item",
        default=lambda self: self._default_product_pricelist_item_id(),
    )
    product_supplierinfo_id = fields.Many2one(
        "product.supplierinfo",
        default=lambda self: self._default_product_supplierinfo_id(),
    )
    product_variant_ids = fields.One2many(
        "product.product",
        "product_tmpl_id",
        related="product_tmpl_id.product_variant_ids",
    )
    selected_packaging_id = fields.Many2one(
        "product.packaging",
        domain="[('product_id', 'in', product_variant_ids)]",
    )
    packaging_price = fields.Float("Package Price", default=0.0, digits="Product Price")
    unit_price = fields.Float(
        "Unit Price",
        compute="_compute_unit_price",
        readonly=True,
        digits="Product Price",
    )
    current_unit_price = fields.Float(
        compute="_compute_current_unit_price", digits="Product Price"
    )
    packaging_ids = fields.One2many(
        "product.packaging",
        string="Product Packages",
        compute="_compute_packaging_ids",
    )
    warning_message = fields.Char(readonly=True, default=" ")

    @api.depends("packaging_price", "selected_packaging_id")
    def _compute_unit_price(self):
        if not self.selected_packaging_id:
            self.unit_price = self.current_unit_price
        elif not self.selected_packaging_id.qty:
            self.unit_price = self.current_unit_price
            self.warning_message = _(
                "Unit price cannot be computed because the selected"
                "packaging has no quantity set."
            )
        else:
            self.unit_price = self.packaging_price / self.selected_packaging_id.qty
            self.warning_message = " "
        self._compute_package_prices()

    @api.depends(
        "product_pricelist_item_id", "product_supplierinfo_id", "product_tmpl_id"
    )
    def _compute_current_unit_price(self):
        """Compute the original unit price, the one  that the calculator will change."""
        if self.product_pricelist_item_id:
            self.current_unit_price = self.product_pricelist_item_id.fixed_price
        elif self.product_supplierinfo_id:
            self.current_unit_price = self.product_supplierinfo_id.price
        elif self.product_id:
            self.current_unit_price = self.product_id.lst_price
        else:
            self.current_unit_price = self.product_tmpl_id.list_price

    @api.depends("unit_price")
    def _compute_package_prices(self):
        for pack in self.packaging_ids:
            pack.packaging_wizard_price = self.unit_price * pack.qty

    @api.depends("product_tmpl_id")
    def _compute_packaging_ids(self):
        self.packaging_ids = self.product_tmpl_id.mapped(
            "product_variant_ids.packaging_ids"
        )

    def action_set_price(self):
        if not self.packaging_price:
            return
        if not self.selected_packaging_id.qty:
            raise UserError(
                _(
                    "Unit price cannot be computed because the selected"
                    "packaging has no quantity set."
                )
            )
        if self.product_pricelist_item_id:
            self.product_pricelist_item_id.fixed_price = self.unit_price
        elif self.product_supplierinfo_id:
            self.product_supplierinfo_id.price = self.unit_price
        elif self.product_id:
            self.product_id.lst_price = self.unit_price
        else:
            self.product_tmpl_id.list_price = self.unit_price

    def reset_unit_price(self):
        xmlid = "product_packaging_unit_price_calculator.action_unit_price_wizard"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        action["context"] = {
            "product_tmpl_id": self._context.get("product_tmpl_id"),
            "active_model": self._context.get("active_model"),
            "active_id": self._context.get("active_id"),
        }
        return action
