# Copyright 2026 Tecnativa - Andrii Kompaniiets
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    discount_type = fields.Selection(
        [("simple", "Simple"), ("range", "By range")], default="simple"
    )
    price_discount = fields.Float(
        compute="_compute_price_discount",
        readonly=False,
        store=True,
    )
    discount_range_ids = fields.One2many(
        "product.pricelist.item.discount_range",
        "pricelist_item_id",
    )

    @api.depends("discount_type")
    def _compute_price_discount(self):
        for record in self:
            if record.discount_type == "range":
                record.price_discount = 0.0

    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        if self.discount_type == "range":
            discount = None
            for discount_range in self.discount_range_ids:
                if discount_range.min <= price <= discount_range.max:
                    discount = discount_range.percentage
                    break
            if discount is not None:
                price = price * (1 - discount / 100) + discount_range.surcharge
            else:
                raise ValidationError(
                    _("Discount range not found for the given price.")
                )
        return super()._compute_price(price, price_uom, product, quantity, partner)

    @api.depends("discount_type", "discount_range_ids")
    def _compute_rule_tip(self):
        base_selection_vals = {
            elem[0]: elem[1]
            for elem in self._fields["base"]._description_selection(self.env)
        }
        for record in self:
            text = ""
            base_amount = 100
            price_surcharge = tools.format_amount(
                record.env, record.price_surcharge, record.currency_id
            )
            if record.discount_type == "range":
                for discount_range in record.discount_range_ids:
                    discount_factor = (100 - discount_range.percentage) / 100
                    discounted_price = base_amount * discount_factor
                    surcharge = tools.format_amount(
                        record.env, discount_range.surcharge, record.currency_id
                    )
                    if record.price_round:
                        discounted_price = tools.float_round(
                            discounted_price, precision_rounding=record.price_round
                        )
                    text += _(
                        "%(base)s from %(min)s to %(max)s: %(discount)s%% "
                        "discount and %(price_surcharge)s extra fee and "
                        "%(surcharge)s surcharge\n"
                        " - Example: %(amount)s * %(discount_charge)s + %(price_surcharge)s + "
                        "%(surcharge)s → %(total_amount)s \n",
                        base=base_selection_vals[record.base],
                        discount=discount_range.percentage,
                        surcharge=surcharge,
                        amount=tools.format_amount(
                            record.env, base_amount, record.currency_id
                        ),
                        discount_charge=discount_factor,
                        price_surcharge=price_surcharge,
                        total_amount=tools.format_amount(
                            record.env,
                            base_amount * (1 - discount_range.percentage / 100)
                            + record.price_surcharge
                            + discount_range.surcharge,
                            record.currency_id,
                        ),
                        min=tools.format_amount(
                            record.env, discount_range.min, record.currency_id
                        ),
                        max=tools.format_amount(
                            record.env, discount_range.max, record.currency_id
                        ),
                    )
                record.rule_tip = text
            else:
                return super(PricelistItem, record)._compute_rule_tip()
