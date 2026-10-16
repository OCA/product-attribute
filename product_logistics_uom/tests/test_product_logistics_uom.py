# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


from unittest.mock import patch

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestProductLogisticsUom(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "product.group_product_manager",
        # The weight and volume units on the product form
        "uom.group_uom",
        # The Inventory page of the product form, when stock is installed
        "stock.group_stock_user",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        config_parameter = cls.env["ir.config_parameter"].sudo()
        config_parameter.set_str("product.weight_in_lbs", "0")
        config_parameter.set_str("product.volume_in_cubic_feet", "0")
        cls.length_uom = cls.env["uom.uom"].create({"name": "Meter"})
        config_parameter.set_int("product_default_length_uom_id", cls.length_uom.id)
        cls.product_template = cls.env["product.template"].create(
            {"name": "Test Product Template"}
        )

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
        with patch.object(
            self.env.registry["product.template"],
            "_calc_volume",
            create=True,
            return_value=1,
        ):
            template.volume = 1
            self.assertEqual(template.product_volume, 1000)

        with patch.object(
            self.env.registry["product.template"],
            "_calc_volume",
            create=True,
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

    def test_template_create_with_product_weight(self):
        product_form = Form(self.env["product.template"])
        product_form.name = "Spice 25 g"
        product_form.weight_uom_id = self.weigh_uom_g
        product_form.product_weight = 25
        template = product_form.save()
        self.assertEqual(template.product_weight, 25)
        self.assertEqual(template.weight, 0.025)
        self.assertEqual(template.product_variant_ids.weight, 0.025)

    def test_template_create_with_product_volume(self):
        template = self.env["product.template"].create(
            {
                "name": "Oil 1 L",
                "volume_uom_id": self.volume_uom_l.id,
                "product_volume": 1,
            }
        )
        self.assertEqual(template.product_variant_ids.volume, 0.001)

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
        # The variants share a weight: the template shows it
        self.assertEqual(template.weight, 10.0)
        self.assertEqual(template.product_weight, 10.0)
        self.assertFalse(template.show_volume_uom_warning)  # for coverage
        self.assertFalse(template.show_weight_uom_warning)  # for coverage
        # Writing the weight on the template updates every variant
        template.weight_uom_id = self.weigh_uom_g
        template.product_weight = 2000
        self.assertEqual(variant.weight, 2.0)
        self.assertEqual(self.product.weight, 2.0)
        template.product_weight = 10000
        template.weight_uom_id = self.weigh_uom_kg
        variant.unlink()
        # Volume calculation from product_dimension module has compatibility issue.
        with patch.object(
            self.env.registry["product.template"],
            "_calc_volume",
            create=True,
            return_value=10.0,
        ):
            self.assertEqual(template.volume, 10.0)
        self.assertEqual(template.weight, 10.0)
        self.assertEqual(template.product_volume, 10.0)
        self.assertEqual(template.product_weight, 10.0)

    def test_get_length_uom_id_from_ir_config_parameter(self):
        uom = self.product_template._get_length_uom_id_from_ir_config_parameter()
        self.assertEqual(uom.id, self.length_uom.id)

    def test_compute_product_volume_single_variant(self):
        self.env["ir.config_parameter"].sudo().set_int(
            "product_default_volume_uom_id", self.volume_uom_l.id
        )
        product_template = self.product_template
        product_template.product_variant_ids.write(
            {"volume": 7.5, "volume_uom_id": self.volume_uom_l.id}
        )
        self.assertEqual(product_template.product_volume, 7.5)

    def test_inverse_product_weight_single_variant(self):
        self.env["ir.config_parameter"].sudo().set_int(
            "product_default_weight_uom_id", self.weigh_uom_kg.id
        )
        product_template = self.product_template
        product_template.product_variant_ids.write(
            {"weight": 5.0, "weight_uom_id": self.weigh_uom_kg.id}
        )
        product_template.write({"weight": 12.0, "weight_uom_id": self.weigh_uom_kg.id})
        self.assertEqual(product_template.product_variant_ids.product_weight, 12.0)
