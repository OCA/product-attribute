# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


from unittest.mock import patch

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.product.models.product_template import (
    ProductTemplate as CoreProductTemplate,
)


class TestProductLogisticsUom(BaseCommon):
    _test_user_groups = None

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
        cls.env["ir.config_parameter"].set_str("product.weight_in_lbs", "0")
        cls.env["ir.config_parameter"].set_str("product.volume_in_cubic_feet", "0")
        cls.length_uom = cls.env.ref("uom.product_uom_meter")
        cls.env["ir.config_parameter"].set_int(
            "product_default_length_uom_id", cls.length_uom.id
        )
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
        self.product.volume = 1
        self.assertEqual(template.product_volume, 1000)
        template.product_volume = 10
        self.assertEqual(self.product.volume, 0.01)
        template.volume_uom_id = self.volume_uom_m3
        self.assertEqual(template.product_volume, self.product.volume)

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
        self.assertEqual(template.volume, 10.0)
        self.assertEqual(template.weight, 10.0)
        self.assertEqual(template.product_volume, 0.0)
        self.assertEqual(template.product_weight, 0.0)
        self.assertFalse(template.show_volume_uom_warning)  # for coverage
        self.assertFalse(template.show_weight_uom_warning)  # for coverage
        variant.unlink()
        self.assertEqual(template.product_volume, 10.0)
        self.assertEqual(template.product_weight, 10.0)

    def test_get_length_uom_id_from_ir_config_parameter(self):
        uom = self.product_template._get_length_uom_id_from_ir_config_parameter()
        self.assertEqual(uom.id, self.length_uom.id)

    def test_get_volume_uom_id_from_ir_config_parameter(self):
        self.env["ir.config_parameter"].set_int(
            "product_default_volume_uom_id", self.volume_uom_l.id
        )
        self.assertEqual(
            self.product_template._get_volume_uom_id_from_ir_config_parameter(),
            self.volume_uom_l,
        )

        with patch.object(
            CoreProductTemplate,
            "_get_volume_uom_id_from_ir_config_parameter",
            return_value=self.volume_uom_m3,
        ):
            self.env["ir.config_parameter"].set_int(
                "product_default_volume_uom_id", 999999
            )
            self.assertEqual(
                self.product_template._get_volume_uom_id_from_ir_config_parameter(),
                self.volume_uom_m3,
            )

    def test_get_weight_uom_id_from_ir_config_parameter(self):
        self.env["ir.config_parameter"].set_int(
            "product_default_weight_uom_id", self.weigh_uom_g.id
        )
        self.assertEqual(
            self.product_template._get_weight_uom_id_from_ir_config_parameter(),
            self.weigh_uom_g,
        )

        with patch.object(
            CoreProductTemplate,
            "_get_weight_uom_id_from_ir_config_parameter",
            return_value=self.weigh_uom_kg,
        ):
            self.env["ir.config_parameter"].set_int(
                "product_default_weight_uom_id", 999999
            )
            self.assertEqual(
                self.product_template._get_weight_uom_id_from_ir_config_parameter(),
                self.weigh_uom_kg,
            )

    def test_get_length_uom_id_from_ir_config_parameter_fallback(self):
        with patch.object(
            CoreProductTemplate,
            "_get_length_uom_id_from_ir_config_parameter",
            return_value=self.length_uom,
        ):
            self.env["ir.config_parameter"].set_int("product_default_length_uom_id", 0)
            self.assertEqual(
                self.product_template._get_length_uom_id_from_ir_config_parameter(),
                self.length_uom,
            )

    def test_get_length_uom_id_from_invalid_config_parameter(self):
        with patch.object(
            CoreProductTemplate,
            "_get_length_uom_id_from_ir_config_parameter",
            return_value=self.length_uom,
        ):
            self.env["ir.config_parameter"].set_int(
                "product_default_length_uom_id", 999999
            )
            self.assertEqual(
                self.product_template._get_length_uom_id_from_ir_config_parameter(),
                self.length_uom,
            )

    def test_get_core_uom_reference_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unsupported unit type"):
            self.product_template._get_core_uom_reference("unknown")

    def test_compatible_uom_domain_without_reference(self):
        empty_uom = self.env["uom.uom"].browse()
        with patch.object(
            type(self.product_template),
            "_get_core_uom_reference",
            return_value=empty_uom,
        ):
            domain = self.product_template._get_compatible_uom_domain("weight")
        self.assertEqual(domain, [("id", "=", False)])

    def test_compute_product_volume_single_variant(self):
        self.env["ir.config_parameter"].set_int(
            "product_default_volume_uom_id", self.volume_uom_l.id
        )
        product_template = self.product_template
        product_template.product_variant_ids.write(
            {"volume": 7.5, "volume_uom_id": self.volume_uom_l.id}
        )
        self.assertEqual(product_template.product_volume, 7.5)

    def test_inverse_product_volume_single_variant(self):
        self.env["ir.config_parameter"].set_int(
            "product_default_volume_uom_id", self.volume_uom_m3.id
        )
        product_template = self.product_template
        product_template.product_variant_ids.write(
            {"volume": 5.0, "volume_uom_id": self.volume_uom_l.id}
        )
        product_template.write(
            {"product_volume": 12.0, "volume_uom_id": self.volume_uom_l.id}
        )
        self.assertEqual(product_template.product_variant_ids.product_volume, 12.0)

    def test_inverse_product_volume_multiple_variants(self):
        template = self.product.product_tmpl_id
        other_variant = self.product.create(
            {"name": "Other Variant", "product_tmpl_id": template.id}
        )
        variants = template.product_variant_ids
        variants.write({"product_volume": 4.0})
        original_values = variants.mapped("product_volume")
        template.product_volume = 15.0
        self.assertEqual(variants.mapped("product_volume"), original_values)
        self.assertIn(other_variant, variants)

    def test_inverse_product_weight_multiple_variants(self):
        template = self.product.product_tmpl_id
        other_variant = self.product.create(
            {"name": "Other Variant", "product_tmpl_id": template.id}
        )
        variants = template.product_variant_ids
        variants.write({"product_weight": 4.0})
        original_values = variants.mapped("product_weight")
        template.product_weight = 15.0
        self.assertEqual(variants.mapped("product_weight"), original_values)
        self.assertIn(other_variant, variants)

    def test_reject_incompatible_product_uoms(self):
        with self.assertRaises(ValidationError):
            self.product.product_tmpl_id.write({"volume_uom_id": self.weigh_uom_kg.id})

    def test_reject_incompatible_default_uoms(self):
        with self.assertRaises(ValidationError):
            self.env["res.config.settings"].create(
                {"product_default_weight_uom_id": self.volume_uom_l.id}
            )

    def test_accept_compatible_default_uoms(self):
        settings = self.env["res.config.settings"].create(
            {
                "product_default_weight_uom_id": self.weigh_uom_g.id,
                "product_default_volume_uom_id": self.volume_uom_l.id,
                "product_default_length_uom_id": self.length_uom.id,
            }
        )
        self.assertTrue(settings)
