import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    def _get_seller_price(self, price_type, currency=False, uom=False, company=False):

        """Extendable hook: use this if you need to fetch
        different price than price unit from the selected
        seller. Useful if you implement different custom
        fields than price unit, like a discounted price unit.

        :param str price_type: a string that must correspond
        to field name you want to retrieve from seller. Only
        numeric fields will be accepted
        :param ID currency: seller currency will be converted
        to param currency
        :param ID uom: product unit of measure
        :param: ID company: overridable company ID, if it is
        different from self.env.company.id
        :return: requested price type if field exists (in the
        model) and it's a numeric field, else return seller
        standard unit price.
        Both returned value will be evaluated for currency
        rate (if currency param is set)"""

        self.ensure_one()
        if not price_type:
            _logger.warning(
                _(
                    "Improper use of function ProductProduct._get_seller_price(): "
                    "provide price_type parameter." % price_type
                )
            )
            return
        try:
            requested_price = self[price_type]
        except KeyError:
            _logger.warning(
                _(
                    "Improper use of function ProductProduct._get_seller_price(): "
                    "field %s not found in model product.supplierinfo." % price_type
                )
            )
            # field doesn't exist in model:
            # make evaluation on seller standard price unit
            requested_price = self.price
        # field exists: check if numeric field and
        # if convert is needed, then return price
        seller_price = self._eval_seller_price_convert(
            price_field=requested_price, currency=currency, company=company
        )

        return seller_price

    def _eval_seller_price_convert(self, price_field, currency, company):
        """Given a currency to compare with seller currency:

        - check if requested field is logically valid to request
        - check if requested field needs to be converted

        :return: requested seller price if valid request.
        If request is not valid (not a numeric field) return
        the standard price unit field and warning in syslog.
        Both returned values will be converted, if necessary.

        :param str price_field: name of field to evaluate
        :param currency: currency to compare with seller currency
        :param company: company if different from self.env.company
        """

        if not isinstance(price_field, (int, float, fields.Monetary, fields.Float)):
            _logger.warning(
                _(
                    "Improper use of function ProductProduct._get_seller_price(): "
                    "the function should be used with numeric values (float,"
                    "fields.Monetary...) not with %s. Seller standard price unit "
                    "will be returned instead of requested one." % type(price_field)
                )
            )
            # requested field exists (on model) but NaN
            requested_price = self.price
        else:
            requested_price = price_field
        if currency:
            # currency set on supplierinfo has priority
            supplier_currency = self.currency_id or self.property_purchase_currency_id
            to_currency = self.env["res.currency"].browse(currency)
            if supplier_currency != to_currency:
                company = self.env["res.company"].browse(company) or self.env.company
                requested_price_converted = self.currency_id._convert(
                    from_amount=requested_price,
                    to_currency=to_currency.id,
                    company=company.id,
                    date=fields.Date.today(),
                )
                return requested_price_converted
        return requested_price

    @api.model
    def _get_supplierinfo_price_type(self):

        """return a different string name than 'price' to
        use it as argument for :meth: _get_seller_price()"""

        return "price"
