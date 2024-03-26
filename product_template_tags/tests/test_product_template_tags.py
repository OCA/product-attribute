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
        cls.tag = cls.env["product.template.tag"].create({"name": "Test Tag"})
        cls.product_attr = cls.env["product.attribute"].create(
            {
                "name": "Test Attrib",
                "value_ids": [
                    (0, 0, {"name": "Test Attrib Value %s" % str(x)}) for x in (1, 2)
                ],
            }
        )
        cls.product_tmpl = cls.env["product.template"].create(
            {
                "name": "Test Product Tmpl",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.product_attr.id,
                            "value_ids": [(6, 0, cls.product_attr.value_ids.ids)],
                        },
                    )
                ],
            }
        )


class TestProductTemplateTag(TestProductTemplateTagBase):
    def test_00_product_template_tag_uniq(self):
        # test same tag and same company
        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["product.template.tag"].create({"name": "Test Tag"})
        # test same tag and different company
        company = self.env["res.company"].create({"name": "Test"})
        vals = {"name": "Test Tag", "company_id": company.id}
        self.assertTrue(self.env["product.template.tag"].create(vals))

    def test_01_tag_propagation_tmpl2prod(self):
        """Test tag propagation from template to products

        On templates where ``tag_propagation = "tmpl2prod"``, setting tags on the
        template should propagate them to all the variants
        """
        tag = self.tag
        template = self.product_tmpl
        variants = template.product_variant_ids
        template.tag_propagation = "tmpl2prod"
        template.tag_ids = tag
        for variant in variants:
            self.assertEqual(variant.tag_ids, tag)
        self.assertEqual(tag.product_tmpl_ids, template)
        self.assertEqual(tag.product_tmpl_count, 1)
        self.assertEqual(tag.product_prod_ids, variants)
        self.assertEqual(tag.product_prod_count, 2)

    def test_02_tag_propagation_prod2tmpl(self):
        """Test tag propagation from products to template

        On templates where ``tag_propagation = "prod2tmpl"``, setting tags on a variant
        should propagate them to the template, not the other variants
        """
        tag = self.tag
        template = self.product_tmpl
        variant_1, variant_2 = template.product_variant_ids
        # Test tag propagation from products to template
        template.tag_propagation = "prod2tmpl"
        variant_1.tag_ids = tag
        self.assertEqual(template.tag_ids, tag)
        self.assertFalse(variant_2.tag_ids)
        self.assertEqual(tag.product_tmpl_ids, template)
        self.assertEqual(tag.product_tmpl_count, 1)
        self.assertEqual(tag.product_prod_ids, variant_1)
        self.assertEqual(tag.product_prod_count, 1)
