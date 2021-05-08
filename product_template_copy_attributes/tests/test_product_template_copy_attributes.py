# Copyright 2020 Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductTemplateCopyAttributes(TransactionCase):

    def setUp(self):
        super().setUp()
        # Customizable Desk
        self.product_template = self.env.ref(
            'product.product_product_4_product_template')

    def test_product_create_with_default_code(self):
        product = self.product_template.copy()
        self.assertEqual(
            len(product.attribute_line_ids),
            len(self.product_template.attribute_line_ids))
