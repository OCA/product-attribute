# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductTemplateTag(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_tmpl = cls.env["product.template"].create({"name": "Test Product"})

    def test_product_template_tag(self):
        product_tmpl_tag = self.env["product.template.tag"].create(
            {"name": "Test Tag", "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])]}
        )
        product_tmpl_tag._compute_products_count()
        self.assertEqual(product_tmpl_tag.products_count, 1)
