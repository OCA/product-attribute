#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import tests
from odoo.tests import Form


class TestCommon(tests.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.formula_price = 12
        attribute_form = Form(cls.env["product.attribute"])
        attribute_form.name = "Test Attribute"
        with attribute_form.value_ids.new() as value:
            value.name = "Test value"
        with attribute_form.value_ids.new() as formula_value:
            formula_value.name = "Test value with formula"
            formula_value.extra_price_formula = "price = %s" % cls.formula_price
        cls.attribute = attribute_form.save()
        cls.attribute_value, cls.formula_attribute_value = cls.attribute.value_ids

        product_template_form = Form(cls.env["product.template"])
        product_template_form.name = "Test Product Template"
        product_template_form.list_price = 0
        with product_template_form.attribute_line_ids.new() as attribute_line:
            attribute_line.attribute_id = cls.attribute
            attribute_line.value_ids.add(cls.attribute_value)
            attribute_line.value_ids.add(cls.formula_attribute_value)
        cls.product_template = product_template_form.save()
        (
            cls.ptav,
            cls.formula_ptav,
        ) = cls.product_template.attribute_line_ids.product_template_value_ids

        cls.products = cls.product_template.product_variant_ids
        cls.formula_product = cls.products.filtered(
            lambda p: cls.formula_ptav in p.product_template_attribute_value_ids
        )
