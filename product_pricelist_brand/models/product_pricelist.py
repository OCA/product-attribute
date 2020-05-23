# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.multi
    def _compute_price_rule(self, products_qty_partner, date=False,
                            uom_id=False):
        """Recompute price after calling the atomic super method for
        getting proper prices when based on product brand.
        """
        rule_obj = self.env['product.pricelist.item']
        result = super(ProductPricelist, self)._compute_price_rule(
            products_qty_partner, date, uom_id)
        # Make sure all rule records are fetched at once at put in cache
        rule_obj.browse(x[1] for x in result.values()).mapped(
            'price_discount')
        for product, qty, partner in products_qty_partner:
            rule = rule_obj.browse(result[product.id][1])
            if rule.applied_on == '2_product_brand' and \
                    rule.brand_id == product.product_brand_id:
                suitable_rule = False
                if not date:
                    date = self._context.get('date') or fields.Date.today()
                date = fields.Date.to_date(date)
                price = product.price_compute('list_price')[product.id]
                qty_uom_id = self._context.get('uom') or product.uom_id.id
                qty_in_product_uom = qty
                if qty_uom_id != product.uom_id.id:
                    try:
                        qty_in_product_uom = self.env['uom.uom'].browse(
                            [self._context['uom']]
                        )._compute_quantity(
                            qty, product.uom_id)
                    except UserError:
                        # Ignored - incompatible UoM in context,
                        # use default product UoM
                        pass

                price_uom = self.env['uom.uom'].browse([qty_uom_id])
                if rule.min_quantity and qty_in_product_uom < rule.min_quantity:
                    continue
                if rule.base == 'pricelist' and rule.base_pricelist_id:
                    price_tmp = \
                        rule.base_pricelist_id._compute_price_rule([(
                            product,
                            qty,
                            partner)], date, uom_id)[product.id][0]
                    price = rule.base_pricelist_id.currency_id._convert(
                        price_tmp, self.currency_id,
                        self.env.user.company_id, date, round=False)
                else:
                    # if base option is public price take sale price else cost
                    # price of product price_compute returns the price in the
                    # context UoM, i.e. qty_uom_id
                    price = product.price_compute(rule.base)[product.id]

                convert_to_price_uom = (
                    lambda price: product.uom_id._compute_price(
                        price, price_uom))

                if price is not False:
                    if rule.compute_price == 'fixed':
                        price = convert_to_price_uom(rule.fixed_price)
                    elif rule.compute_price == 'percentage':
                        price = (
                            price - (price * (rule.percent_price / 100))) or 0.0
                    else:
                        # complete formula
                        price_limit = price
                        price = (
                            price - (price * (rule.price_discount / 100))) or 0.0
                        if rule.price_round:
                            price = tools.float_round(
                                price, precision_rounding=rule.price_round)

                        if rule.price_surcharge:
                            price_surcharge = convert_to_price_uom(
                                rule.price_surcharge)
                            price += price_surcharge

                        if rule.price_min_margin:
                            price_min_margin = convert_to_price_uom(
                                rule.price_min_margin)
                            price = max(price, price_limit + price_min_margin)

                        if rule.price_max_margin:
                            price_max_margin = convert_to_price_uom(
                                rule.price_max_margin)
                            price = min(price, price_limit + price_max_margin)
                    suitable_rule = rule
                # Final price conversion into pricelist currency
                if suitable_rule and price and \
                        suitable_rule.compute_price != 'fixed' and \
                        suitable_rule.base != 'pricelist':
                    if suitable_rule.base == 'standard_price':
                        cur = product.cost_currency_id
                    else:
                        cur = product.currency_id
                    price = cur._convert(price, self.currency_id,
                                         self.env.user.company_id,
                                         date, round=False)

                if price:
                    result[product.id] = (
                        price, suitable_rule and suitable_rule.id or False)
        return result


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    applied_on = fields.Selection(selection_add=[
        ("2_product_brand", "Product Brand")])
    brand_id = fields.Many2one(
        'product.brand', 'Product Brand', ondelete='cascade',
        help="Specify a product brand if this rule only applies to products "
             "belonging to this brand. Keep empty otherwise.")

    @api.multi
    @api.depends('brand_id', 'categ_id', 'product_tmpl_id', 'product_id',
                 'compute_price', 'fixed_price', 'pricelist_id',
                 'percent_price', 'price_discount', 'price_surcharge')
    def _get_pricelist_item_name_price(self):
        self.ensure_one()
        super(ProductPricelistItem, self)._get_pricelist_item_name_price()
        if self.brand_id:
            self.name = _("Brand: %s") % (self.brand_id.name)

    @api.onchange('applied_on')
    def _onchange_applied_on(self):
        super(ProductPricelistItem, self)._onchange_applied_on()

        if self.applied_on != '2_product_brand':
            self.brand_id = False
