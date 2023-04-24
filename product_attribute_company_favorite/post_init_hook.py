import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def initialize_attribute_is_favorite_field(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env["res.company"].with_context(active_test=False).search([]):
        _logger.info("Configure is_favorite field for the company %s" % (company.name))
        product_attributes = (
            env["product.attribute"].sudo().with_company(company.id).search([])
        )
        product_attributes.write({"is_favorite": True})

        product_attribute_values = (
            env["product.attribute.value"].sudo().with_company(company.id).search([])
        )
        product_attribute_values.write({"is_favorite": True})
