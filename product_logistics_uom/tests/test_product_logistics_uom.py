# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


from unittest.mock import patch

from odoo.tests.common import TransactionCase


class TestProductLogisticsUom(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )
        cls.weigh_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.weigh_uom_g = cls.env.ref("uom.product_uom_gram")
        cls.volume_uom_m3 = cls.env.ref("uom.product_uom_cubic_meter")
        cls.volume_uom_l = cls.env.ref("uom.product_uom_litre")
        # set volume in m3 and weight in kg
        cls.env["ir.config_parameter"].set_param("product.weight_in_lbs", "0")
        cls.env["ir.config_parameter"].set_param("product.volume_in_cubic_feet", "0")

    def test_product_volume(self):
        self.product.volume_uom_id = self.volume_uom_l
        self.product.volume = 1
        self.assertEqual(self.product.product_volume, 1000)
        self.product.product_volume = 10
        self.assertEqual(self.product.volume, 0.01)
        self.product.volume_uom_id = self.volume_uom_m3
        self.assertEqual(self.product.product_volume, self.product.volume)

    def test_product_show_product_uom_warning(self):
        self.product.volume_uom_id = self.volume_uom_m3
        self.product.volume = 0.0001
        self.assertTrue(self.product.show_volume_uom_warning)
        self.product.volume_uom_id = self.volume_uom_l
        self.assertFalse(self.product.show_volume_uom_warning)

    def test_product_weight(self):
        self.product.weight_uom_id = self.weigh_uom_g
        self.product.weight = 1
        self.assertEqual(self.product.product_weight, 1000)
        self.product.product_weight = 10
        self.assertEqual(self.product.weight, 0.01)
        self.product.weight_uom_id = self.weigh_uom_kg
        self.assertEqual(self.product.product_weight, self.product.weight)

    def test_product_show_product_weight_warning(self):
        self.product.weight_uom_id = self.weigh_uom_kg
        self.product.weight = 0.0001
        self.assertTrue(self.product.show_weight_uom_warning)
        self.product.weight_uom_id = self.weigh_uom_g
        self.assertFalse(self.product.show_weight_uom_warning)

    def test_template_volume(self):
        template = self.product.product_tmpl_id
        template.volume_uom_id = self.volume_uom_l
        # Volume calculation from product_dimension module has compatibility issue.
        with patch(
            "odoo.addons.product_dimension.models.product_template.ProductTemplate._calc_volume",
            return_value=1,
        ):
            template.volume = 1
            self.assertEqual(template.product_volume, 1000)

        with patch(
            "odoo.addons.product_dimension.models.product_template.ProductTemplate._calc_volume",
            return_value=0.01,
        ):
            template.product_volume = 10
            self.assertEqual(template.volume, 0.01)
        template.volume_uom_id = self.volume_uom_m3
        self.assertEqual(template.product_volume, template.volume)

    def test_template_show_volume_uom_warning(self):
        template = self.product.product_tmpl_id
        template.volume_uom_id = self.volume_uom_m3
        template.volume = 0.0001
        self.assertTrue(template.show_volume_uom_warning)
        template.volume_uom_id = self.volume_uom_l
        self.assertFalse(template.show_volume_uom_warning)

    def test_template_weight(self):
        template = self.product.product_tmpl_id
        template.weight_uom_id = self.weigh_uom_g
        template.weight = 1
        self.assertEqual(template.product_weight, 1000)
        template.product_weight = 10
        self.assertEqual(template.weight, 0.01)
        template.weight_uom_id = self.weigh_uom_kg
        self.assertEqual(template.product_weight, template.weight)

    def test_template_show_weight_uom_warning(self):
        template = self.product.product_tmpl_id
        template.weight_uom_id = self.weigh_uom_kg
        template.weight = 0.0001
        self.assertTrue(template.show_weight_uom_warning)
        template.weight_uom_id = self.weigh_uom_g
        self.assertFalse(template.show_weight_uom_warning)

    def test_template_with_variant(self):
        variant = self.product.create(
            {"name": "Test Variant", "product_tmpl_id": self.product.product_tmpl_id.id}
        )
        template = self.product.product_tmpl_id
        variant.product_volume = 10
        variant.product_weight = 10
        self.product.product_volume = 10
        self.product.product_weight = 10
        self.assertEqual(template.volume, 0.0)
        self.assertEqual(template.volume, 0.0)
        self.assertEqual(template.product_volume, 0.0)
        self.assertEqual(template.product_weight, 0.0)
        self.assertFalse(template.show_volume_uom_warning)  # for coverage
        self.assertFalse(template.show_weight_uom_warning)  # for coverage
        variant.unlink()
        # Volume calculation from product_dimension module has compatibility issue.
        with patch(
            "odoo.addons.product_dimension.models.product_template.ProductTemplate._calc_volume",
            return_value=10.0,
        ):
            self.assertEqual(template.volume, 10.0)
        self.assertEqual(template.weight, 10.0)
        self.assertEqual(template.product_volume, 10.0)
        self.assertEqual(template.product_weight, 10.0)
