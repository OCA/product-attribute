# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestProductManufacturer(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.manufacturer_a = cls.env["res.partner"].create({"name": "Manufacturer A"})
        cls.manufacturer_b = cls.env["res.partner"].create({"name": "Manufacturer B"})
        cls.attr1 = cls.env["product.attribute"].create({"name": "color"})
        cls.attr1_1 = cls.env["product.attribute.value"].create(
            {"name": "red", "attribute_id": cls.attr1.id}
        )
        cls.attr1_2 = cls.env["product.attribute.value"].create(
            {"name": "blue", "attribute_id": cls.attr1.id}
        )
        cls.product1 = cls.env["product.template"].create(
            {
                "name": "Test Product Manufacturer 1",
            }
        )

    def test_01_product_manufacturer(self):
        self.product1.update(
            {
                "manufacturer": self.manufacturer_a.id,
                "manufacturer_pname": "Test Product A",
                "manufacturer_pref": "TPA",
                "manufacturer_purl": "https://www.manufacturera.com/test_product_a",
            }
        )

        self.assertEqual(
            self.product1.product_variant_id.manufacturer.id, self.manufacturer_a.id
        )
        self.assertEqual(
            self.product1.product_variant_id.manufacturer_pname, "Test Product A"
        )
        self.assertEqual(self.product1.product_variant_id.manufacturer_pref, "TPA")
        self.assertEqual(
            self.product1.product_variant_id.manufacturer_purl,
            "https://www.manufacturera.com/test_product_a",
        )

    def test_02_product_manufacturer(self):
        self.product1.update(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attr1.id,
                            "value_ids": [(6, 0, [self.attr1_1.id, self.attr1_2.id])],
                        },
                    ),
                ],
            }
        )
        self.product1.product_variant_ids[0].update(
            {
                "manufacturer": self.manufacturer_b.id,
                "manufacturer_pname": "Test Product B",
                "manufacturer_pref": "TPB",
                "manufacturer_purl": "https://www.manufacturerb.com/test_product_b",
            }
        )
        self.product1.product_variant_ids[1].update(
            {
                "manufacturer": self.manufacturer_a.id,
                "manufacturer_pname": "Test Product A",
                "manufacturer_pref": "TPA",
                "manufacturer_purl": "https://www.manufacturera.com/test_product_a",
            }
        )
        self.assertEqual(self.product1.manufacturer.id, False)
        self.assertEqual(self.product1.manufacturer_pname, False)
        self.assertEqual(self.product1.manufacturer_pref, False)
        self.assertEqual(self.product1.manufacturer_purl, False)
        self.assertEqual(
            self.product1.product_variant_ids[1].manufacturer.id, self.manufacturer_a.id
        )
        self.assertEqual(
            self.product1.product_variant_ids[1].manufacturer_pname, "Test Product A"
        )
        self.assertEqual(self.product1.product_variant_ids[1].manufacturer_pref, "TPA")
        self.assertEqual(
            self.product1.product_variant_ids[1].manufacturer_purl,
            "https://www.manufacturera.com/test_product_a",
        )
        self.assertEqual(
            self.product1.product_variant_ids[0].manufacturer.id, self.manufacturer_b.id
        )
        self.assertEqual(
            self.product1.product_variant_ids[0].manufacturer_pname, "Test Product B"
        )
        self.assertEqual(self.product1.product_variant_ids[0].manufacturer_pref, "TPB")
        self.assertEqual(
            self.product1.product_variant_ids[0].manufacturer_purl,
            "https://www.manufacturerb.com/test_product_b",
        )

    def test_03_product_manufacturer_creation(self):
        new_pt = self.env["product.template"].create(
            {
                "name": "New Product Template",
                "manufacturer": self.manufacturer_a.id,
                "manufacturer_pname": "Test Product A",
                "manufacturer_pref": "TPA",
                "manufacturer_purl": "https://www.manufacturera.com/test_product_a",
            }
        )

        self.assertEqual(
            new_pt.product_variant_id.manufacturer.id, new_pt.manufacturer.id
        )
        self.assertEqual(
            new_pt.product_variant_id.manufacturer_pname, new_pt.manufacturer_pname
        )
        self.assertEqual(
            new_pt.product_variant_id.manufacturer_pref, new_pt.manufacturer_pref
        )
        self.assertEqual(
            new_pt.product_variant_id.manufacturer_purl, new_pt.manufacturer_purl
        )
