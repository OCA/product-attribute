# Copyright (C) 2026 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        # Override name_search to prioritize default_code search.
        # If results are found by default_code, return them.
        # Otherwise, continue with super() search.
        domain = list(domain or [])

        if name:
            # First try to search by default_code
            domain_args = domain + [("default_code", operator, name)]
            code_results = self._search(domain_args, limit=limit, order=order)

            if code_results:
                # If we found results by code, return them as list of IDs
                return list(code_results)

        # If no code results or no name provided, use super() search
        return super()._name_search(
            name=name, domain=domain, operator=operator, limit=limit, order=order
        )


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        # Override name_search to prioritize default_code search.
        # If results are found by default_code, return them.
        # Otherwise, continue with super() search.
        domain = list(domain or [])

        if name:
            # First try to search by default_code
            domain_args = domain + [("default_code", operator, name)]
            code_results = self._search(domain_args, limit=limit, order=order)

            if code_results:
                # If we found results by code, return them as list of IDs
                return list(code_results)

        # If no code results or no name provided, use super() search
        return super()._name_search(
            name=name, domain=domain, operator=operator, limit=limit, order=order
        )
