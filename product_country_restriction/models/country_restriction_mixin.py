# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CountryRestrictionMixin(models.AbstractModel):

    _name = 'country.restriction.mixin'

    @api.multi
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

    @api.multi
    def _get_country_restrictions(
            self,
            countries,
            date=False,
            restriction_id=False):
        if not date:
            date = fields.Date.today()
        product_by_country = {}
        for country in countries:
            product_by_country.update({
                country: self
            })
        res = self.env['product.country.restriction']._get_restriction(
            product_by_country=product_by_country,
            date=date,
            restriction_id=restriction_id,
        )
        return res
