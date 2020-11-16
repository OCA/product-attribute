# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger


class TestProductTemplateTagBase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_tmpl = cls.env["product.template"].create({"name": "Test Product"})


class TestProductTemplateTag(TestProductTemplateTagBase):
    def test_product_template_tag(self):
        product_tmpl_tag = self.env["product.template.tag"].create(
            {"name": "Test Tag", "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])]}
        )
        product_tmpl_tag._compute_products_count()
        self.assertEqual(product_tmpl_tag.products_count, 1)

    def test_product_template_tag_uniq(self):
        product_tmpl_tag = self.env["product.template.tag"].create({"name": "Test Tag"})
        self.assertTrue(product_tmpl_tag)
        # test same tag and same company
        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["product.template.tag"].create({"name": "Test Tag"})

        # test same tag and different company
        company = self.env["res.company"].create({"name": "Test"})
        same_product_tmpl_tag_diff_company = self.env["product.template.tag"].create(
            {"name": "Test Tag", "company_id": company.id}
        )
        self.assertTrue(same_product_tmpl_tag_diff_company)
