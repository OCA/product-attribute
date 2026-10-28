# Copyright 2026 360ERP (<https://www.360erp.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.model
    def _get_cost_security_default_price_product(self):
        """Return the product whose cost is used as default vendor price."""
        ctx = self.env.context
        if ctx.get("product_cost_security_product_id"):
            return self.env["product.product"].browse(
                ctx["product_cost_security_product_id"]
            )
        if ctx.get("default_product_tmpl_id"):
            return self.env["product.template"].browse(ctx["default_product_tmpl_id"])
        return self.env["product.template"]

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if "price" not in fields or "default_price" in self.env.context:
            return res
        product = self._get_cost_security_default_price_product()
        if product and product._has_field_access(
            product._fields["standard_price"], "read"
        ):
            res["price"] = product.standard_price
        return res
