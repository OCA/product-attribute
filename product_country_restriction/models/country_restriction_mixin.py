# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CountryRestrictionMixin(models.AbstractModel):

    _name = "country.restriction.mixin"
    _description = "Country Restriction Mixin"

    def _has_country_restriction(self, countries, date=False):
        """
        For one product, get if it has country embargo
        :param countries:
        :param date:
        :return: boolean
        """
        self.ensure_one()
        if not date:
            date = fields.Date.today()
        res = self._get_country_restrictions(countries, date=date)
        if self in res:
            return res
        return {}

    def _get_country_restrictions(self, countries, date=False, restriction_id=False):
        if not date:
            date = fields.Date.today()
        product_by_country = {}
        for country in countries:
            product_by_country.update({country: self})
        res = self.env["product.country.restriction"]._get_restriction(
            product_by_country=product_by_country,
            date=date,
            restriction_id=restriction_id,
        )
        res = self._update_country_strategy(res)
        return res

    def _update_country_strategy(self, result):
        """
        This is used to apply another strategy to the rules result
        depending on company strategy
        :return:
        """
        company = self.env.company
        if hasattr(self, "company_id") and self.company_id:
            company = self.company_id
        strategy = company.country_restriction_strategy

        if strategy == "authorize":
            # The default strategy that authorizes all products
            return result
        elif strategy == "restrict":
            # The strategy that restricts all products but those with
            # applied rules
            applied_products = result.keys()
            result = {}
            for product in self.filtered(lambda p, ap=applied_products: p not in ap):
                result.update(
                    {
                        product: False,
                    }
                )
        return result
