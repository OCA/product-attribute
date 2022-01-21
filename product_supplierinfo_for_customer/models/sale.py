from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        # Required when using product configurator.
        # need to provide partner_id to name_get
        # to get SOL name = partner product name
        new_context = dict(self._context)
        new_context["partner_id"] = self.order_id.partner_id.id
        super(SaleOrderLine, self.with_context(new_context)).product_id_change()
