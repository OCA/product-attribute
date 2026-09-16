# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_country_restriction_country(self):
        self.ensure_one()
        partner = self.order_id.partner_shipping_id or self.order_id.partner_id
        return partner.country_id

    def _get_country_restriction_date(self):
        self.ensure_one()
        return fields.Date.to_date(self.order_id.date_order) or fields.Date.today()

    def _get_country_restriction_warning(self):
        self.ensure_one()
        country = self._get_country_restriction_country()
        if not self.product_id or not country:
            return {}
        restrictions = self.product_id._get_country_restrictions(
            country,
            date=self._get_country_restriction_date(),
        )
        message = self.env[
            "product.country.restriction"
        ]._get_country_restriction_messages(restrictions)
        if not message:
            return {}
        return {
            "title": _("Country Restriction"),
            "message": message,
        }

    @api.onchange("product_id")
    def _onchange_product_id_warning(self):
        res = super()._onchange_product_id_warning()
        warning = self._get_country_restriction_warning()
        if not warning:
            return res
        if not res:
            res = {}
        if res.get("warning"):
            warning["message"] = "\n\n".join(
                [
                    res["warning"].get("message", ""),
                    warning["message"],
                ]
            )
        res["warning"] = warning
        return res
