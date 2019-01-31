# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCountryRestrictionRule(models.Model):

    _name = 'product.country.restriction.rule'
    _description = 'Product Country Restriction Rule'
    _order = 'sequence asc, id desc'

    name = fields.Char(
        required=True,
        translate=True
    )
    code = fields.Char(
        required=True,
    )
    sequence = fields.Integer(
        default=10,
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE (code)',
         'Product Country Restriction Rule Code has to be unique !'),
    ]

    @api.model
    def _get_by_code(self, code):
        return self.search([('code', '=', code)], limit=1)

    def _apply(self, products, item):
        """
        Look for existing rule method and return a dict with products
        that trigger the rule
        :param products:
        :param item:
        :return:
        """
        self.ensure_one()
        res = {}
        method = '_apply_rule_%s' % self.code
        if hasattr(self, method):
            res = getattr(self, method)(products, item)
        return res

    def _apply_rule_global(self, products, item):
        """
        Return all products as this is a global rule
        :param products:
        :param item:
        :return:
        """
        res = set()
        for product in products:
            res.add(product)
        return res

    def _apply_rule_category(self, products, item):
        """
        Parse all categories in products
        :param products:
        :param item:
        :return:
        """
        res = set()
        if item.product_category_id:
            for product in products:
                category_id = product.categ_id
                while category_id:
                    if category_id == item.product_category_id:
                        res.add(product)
                        break
                    category_id = category_id.parent_id
        return res

    def _apply_rule_product(self, products, item):
        """
        Apply rule on templates and on all its variants
        :param products:
        :param item:
        :return:
        """
        res = set()
        if products and products[0]._name == 'product.template':
            for product in products.filtered(
                    lambda p: p.id == item.product_template_id.id):
                res.add(product)
        elif products and products[0]._name == 'product.product':
            for product in products.filtered(
                    lambda p: p.product_tmpl_id == item.product_template_id):
                res.add(product)
        return res

    def _apply_rule_variant(self, products, item):
        """
        Get all matching product variants
        :param products:
        :param item:
        :return:
        """
        res = set()
        if products and products[0]._name == 'product.product':
            for product in products.filtered(
                    lambda p: p.id == item.product_id.id):
                res.add(product)
        return res
