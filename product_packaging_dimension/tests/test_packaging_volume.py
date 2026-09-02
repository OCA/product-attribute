# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPackagingVolumeCompute(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Prepare reusable UoM records used by packaging volume tests
        cls.icp = cls.env["ir.config_parameter"].sudo()
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.uom_m = cls.env.ref("uom.product_uom_meter")
        cls.uom_mm = cls.env.ref("uom.product_uom_millimeter")
        cls.uom_m3 = cls.env.ref("uom.product_uom_cubic_meter")
        cls.uom_ft = cls.env.ref("uom.product_uom_foot")
        cls.uom_ft3 = cls.env.ref("uom.product_uom_cubic_foot")
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_lb = cls.env.ref("uom.product_uom_lb")

    def _set_uom_config(self, volume_in_cubic_feet=False, weight_in_lbs=False):
        """Set standard UoM config parameters."""
        self.icp.set_param("product_default_length_uom_id", False)
        self.icp.set_param("product_default_volume_uom_id", False)
        self.icp.set_param("product_default_weight_uom_id", False)
        self.icp.set_param(
            "product.volume_in_cubic_feet",
            "1" if volume_in_cubic_feet else False,
        )
        self.icp.set_param("product.weight_in_lbs", "1" if weight_in_lbs else False)

    def _create_packaging(self, length, height, width, product_volume=0.0):
        """Create a product packaging with explicit dimensions."""
        product = self.env["product.product"].create(
            {
                "name": "Product with packaging dimensions",
                "uom_id": self.uom_unit.id,
                "volume": product_volume,
            }
        )
        return self.env["product.packaging"].create(
            {
                "product_id": product.id,
                "uom_id": self.uom_dozen.id,
                "packaging_length": length,
                "height": height,
                "width": width,
            }
        )

    def _get_expected_volume(self, packaging):
        """Compute expected dimensional volume with configured UoM helpers."""
        product_template = self.env["product.template"]
        length_uom = product_template._get_length_uom_id_from_ir_config_parameter()
        volume_uom = product_template._get_volume_uom_id_from_ir_config_parameter()
        uom_m3 = self.env.ref("uom.product_uom_cubic_meter")
        length_m = length_uom._compute_quantity(
            packaging.packaging_length,
            self.uom_m,
            round=False,
        )
        height_m = length_uom._compute_quantity(
            packaging.height,
            self.uom_m,
            round=False,
        )
        width_m = length_uom._compute_quantity(
            packaging.width,
            self.uom_m,
            round=False,
        )
        return volume_uom.round(
            uom_m3._compute_quantity(
                length_m * height_m * width_m,
                volume_uom,
                round=False,
            )
        )

    def _assert_dimensional_volume(self, packaging):
        """Assert packaging volume matches dimensional calculation."""
        product_template = self.env["product.template"]
        volume_uom = product_template._get_volume_uom_id_from_ir_config_parameter()
        expected = self._get_expected_volume(packaging)
        self.assertEqual(volume_uom.compare(expected, packaging.volume), 0)

    def assert_product_packaging_volume(self, expected, packaging):
        """Assert packaging volume matches the product packaging path."""
        volume_uom = self.env[
            "product.template"
        ]._get_volume_uom_id_from_ir_config_parameter()
        self.assertEqual(volume_uom.compare(expected, packaging.volume), 0)

    def test_input_uom(self):
        """Check dimensional volume with Odoo core length UoM settings."""
        self._set_uom_config()
        packaging = self._create_packaging(10.0, 10.0, 10.0)
        self._assert_dimensional_volume(packaging)

        self._set_uom_config(volume_in_cubic_feet=True)
        packaging = self._create_packaging(10.0, 10.0, 10.0)
        self._assert_dimensional_volume(packaging)

    def test_compute_volume(self):
        """Check dimensional volume with different complete dimensions."""
        self._set_uom_config()

        packaging = self._create_packaging(10.0, 8.0, 10.0)
        self._assert_dimensional_volume(packaging)

        packaging = self._create_packaging(6.0, 14.0, 1.0)
        self._assert_dimensional_volume(packaging)

        packaging = self._create_packaging(100.0, 50.0, 80.0)
        self._assert_dimensional_volume(packaging)

    def test_compute_volume_branches(self):
        """Check base, partial-dimension, and full-dimension compute branches."""
        self._set_uom_config()

        packaging = self._create_packaging(0.0, 0.0, 0.0, product_volume=2.5)
        self.assert_product_packaging_volume(
            packaging.product_id.volume * packaging.qty, packaging
        )

        packaging = self._create_packaging(10.0, 0.0, 0.0, product_volume=2.5)
        self.assert_product_packaging_volume(0.0, packaging)

        packaging = self._create_packaging(10.0, 8.0, 10.0, product_volume=2.5)
        self._assert_dimensional_volume(packaging)

    def test_output_uom(self):
        """Check dimensional volume with Odoo core volume UoM settings."""
        self._set_uom_config()
        packaging = self._create_packaging(10.0, 10.0, 10.0)
        self._assert_dimensional_volume(packaging)

        self._set_uom_config(volume_in_cubic_feet=True)
        packaging = self._create_packaging(10.0, 10.0, 10.0)
        self._assert_dimensional_volume(packaging)

    def test_uom_names_come_from_config_parameters(self):
        """Check displayed UoM names come from Odoo core UoM settings."""
        self._set_uom_config()
        packaging = self._create_packaging(1.0, 1.0, 1.0)
        self.assertEqual(packaging.length_uom_name, self.uom_mm.display_name)
        self.assertEqual(packaging.volume_uom_name, self.uom_m3.display_name)
        self.assertEqual(packaging.weight_uom_name, self.uom_kg.display_name)

        self._set_uom_config(volume_in_cubic_feet=True, weight_in_lbs=True)
        packaging = self._create_packaging(1.0, 1.0, 1.0)
        self.assertEqual(packaging.length_uom_name, self.uom_ft.display_name)
        self.assertEqual(packaging.volume_uom_name, self.uom_ft3.display_name)
        self.assertEqual(packaging.weight_uom_name, self.uom_lb.display_name)
