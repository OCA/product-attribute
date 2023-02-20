import logging
import traceback

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    @api.depends("product_tmpl_id.seller_ids", "product_id.seller_ids")
    def _compute_product_pricelist_selling_price(self):
        # add seller_ids to dependencies to recompute the
        # selling price in case fields have store=True
        return super()._compute_product_pricelist_selling_price()

    def _set_product_pricelist_selling_price(self, product_price, product):
        if self.base == "supplierinfo":
            # no need to call _compute_price(), actually it would show
            # inconsistent outcome because price would be computed twice
            self.product_pricelist_selling_price = product_price
        else:
            return super()._set_product_pricelist_selling_price(
                product_price=product_price, product=product
            )

    @api.model
    def _get_allowed_base_rule(self):

        """Add supplierinfo key. This method is here to avoid
        key errors in price_compute() call on main compute method.
        Only allowed key will re-trigger price recomputation."""

        return super()._get_allowed_base_rule() + ["supplierinfo"]

    def _get_product_price_rule_base(self, product):
        """
        Inheritable method to compute and return selling
        price, depending on 'based on' parameter.
        Depending on 'base' we might want to use another
        method, change context, use different args...

        @Override: return product price in the context
        of a pricelist-rule based on supplierinfo price
        after pricelist rule is applied. Keeps User
        Interface responsive for @api.depends.

        :param product: product linked to pricelist-rule

        :returns:
        - product price (computed by rule parameters)
        - False if it's not possible to compute price rule
        for selected product
        """

        product_price = super()._get_product_price_rule_base(product=product)

        if self.compute_price == "formula" and self.base == "supplierinfo":

            if product._name == "product.template":
                product = product.product_variant_id

            # Hook to get params: these params will be propagated
            # to _prepare_seller to manage multiple seller currency
            # conversion before seller fetching, see:
            # https://github.com/OCA/product-attribute/pull/1311
            params = product._get_select_seller_params(
                self, date=None, quantity=0.0, product_id=None
            )

            # We prefer the usage of _compute_price() over _compute_price_rule()
            # (or other method that will be called on ProductPricelist) because
            # it's the only way to have responsive UI (otherwise UI will update
            # only when the whole product record get saved).
            # We must use lower level approach at this point, because if we call
            # _get_supplierinfo_pricelist_price, the price returned will already
            # have pricelist-rule applied and result will be inconsistent. In
            # order to provide a responsive UI and give consistent results we
            # have to call _select_seller into _compute_price

            seller_price = self._fetch_supplierinfo_price(
                product=product, params=params
            )

            # _compute_price(): UI responsive on @api.depends
            product_price = self._compute_price(
                price=seller_price,
                price_uom=product.uom_id,
                product=product,
                quantity=self.min_quantity,
                partner=self.filter_supplier_id,
            )

        return product_price

    def _get_percent_change_rule_base(self, product):

        """@override: compute discount percentage based on user
        input and computed selling price, for pricelists based
        on supplierinfo prices

         :returns dictionary 'discount' with two keys:

        * 'discount_field_name': the field on which percent change applies
        (can be 'price_discount' or 'percent_price')

        * 'discount': percentage change computed by formula:

         ``(input - computed selling price) / computed selling price x 100``
        """

        discount = super()._get_percent_change_rule_base(product=product)

        if self.compute_price == "formula" and self.base == "supplierinfo":

            if product._name == "product.template":
                product = product.product_variant_id

            # Hook to get params: these params will be propagated
            # to _prepare_seller to manage multiple seller currency
            # conversion before seller fetching, see:
            # https://github.com/OCA/product-attribute/pull/1311
            params = product._get_select_seller_params(
                self, date=None, quantity=0.0, product_id=None
            )

            # _compute_price() is the only UI responsive method for @api.depends,
            # so we must go low level, see _get_product_price_rule_base for info

            seller_price = self._fetch_supplierinfo_price(
                product=product, params=params
            )

            discount["discount_field_name"] = "price_discount"
            discount["product_price"] = seller_price

        return discount

    def set_percentage_change(self):

        """Inheritable method: make checks before the assignement
        of % discount or change fetch for the price based on rule setup"""

        if self.base == "supplierinfo":
            discount_dict = self._get_percentage_change()
            self._manage_percent_change_user_input_errors(discount_dict)
            # no user input error on input field, try to set the % field
            price = discount_dict.get("product_price")

            try:
                discount = ((price - self.percent_change_user_input) / price) * 100
            except ZeroDivisionError:
                raise UserError(
                    _(
                        "Supplier provided purchase price is equal to 0.00.\n"
                        "Cannot divide by zero, please correct parameters and try again.\n\n%s"
                        "Hint: if provided values are correct try to save unsaved records and "
                        "try again." % (traceback.format_exc())
                    )
                )
            discount_field_name = discount_dict.get("discount_field_name")
            if discount_field_name and discount:
                self[discount_field_name] = discount
            # reset input value, after correct execution
            self._reset_percent_change_user_input()
            return
        return super().set_percentage_change()

    def _fetch_supplierinfo_price(self, product, params):

        """Low level method: call _select_seller and return
         a specific seller price before the pricelist-rule
         is applied on it.

        :param product: product in the context of a pricelist
        rule that has to be searched on in order to fetch the
        proper requested related seller prices

        :param dict params: params that will be propagated to
        _select_seller and _prepare_seller methods

        :return float: seller price before rule computation
        """

        seller_id = product.with_context(
            override_min_qty=self.no_supplierinfo_min_quantity,
        )._select_seller(
            partner_id=self.filter_supplier_id,
            quantity=self.min_quantity,
            date=None,
            params=params,
        )

        # use provided params or fetch
        pricelist_currency = (
            params.get("to_currency")
            or self.currency_id
            or self.pricelist_id.currency_id
        )

        company = params.get("company") or self.env.company

        if not seller_id:
            return 0.0

        # override to fetch different prices from seller (custom fields..)
        price_type = seller_id._get_supplierinfo_price_type()

        # We got the proper seller, but we can't use price_compute()
        # to retrieve the 'vanilla' supplierinfo price since it would
        # return a dummy price of 1.0. This means that we have to
        # explicitly deal with currency rate (again) in case seller
        # currency is different.
        seller_price = seller_id._get_seller_price(
            price_type=price_type,
            currency=pricelist_currency,
            uom=False,
            company=company,
        )

        return seller_price
