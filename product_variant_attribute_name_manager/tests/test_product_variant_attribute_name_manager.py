# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductTemplateAttributeValue(TransactionCase):
    def setUp(self):
        super(TestProductTemplateAttributeValue, self).setUp()

        self.computer = self.env["product.template"].create(
            {"name": "Super Computer", "price": 2000}
        )

        self._add_ssd_attribute()
        self._add_ram_attribute()
        self._add_hdd_attribute()

    def _add_ssd_attribute(self):
        self.ssd_attribute = self.env["product.attribute"].create(
            {
                "name": "Memory",
                "short_name": "Mem",
                "display_attribute_name": True,
                "sequence": 1,
            }
        )
        self.ssd_256 = self.env["product.attribute.value"].create(
            {"name": "256 GB", "attribute_id": self.ssd_attribute.id, "sequence": 1}
        )
        self.ssd_512 = self.env["product.attribute.value"].create(
            {"name": "512 GB", "attribute_id": self.ssd_attribute.id, "sequence": 2}
        )

        self.computer_ssd_attribute_lines = self.env[
            "product.template.attribute.line"
        ].create(
            {
                "product_tmpl_id": self.computer.id,
                "attribute_id": self.ssd_attribute.id,
                "value_ids": [(6, 0, [self.ssd_256.id, self.ssd_512.id])],
                "sequence": 2,
            }
        )

    def _add_ram_attribute(self):
        self.ram_attribute = self.env["product.attribute"].create(
            {"name": "RAM", "display_attribute_name": True, "sequence": 2}
        )
        self.ram_8 = self.env["product.attribute.value"].create(
            {"name": "8 GB", "attribute_id": self.ram_attribute.id, "sequence": 1}
        )
        self.ram_16 = self.env["product.attribute.value"].create(
            {"name": "16 GB", "attribute_id": self.ram_attribute.id, "sequence": 2}
        )
        self.ram_32 = self.env["product.attribute.value"].create(
            {"name": "32 GB", "attribute_id": self.ram_attribute.id, "sequence": 3}
        )
        self.computer_ram_attribute_lines = self.env[
            "product.template.attribute.line"
        ].create(
            {
                "product_tmpl_id": self.computer.id,
                "attribute_id": self.ram_attribute.id,
                "value_ids": [(6, 0, [self.ram_8.id, self.ram_16.id, self.ram_32.id])],
                "sequence": 3,
            }
        )

    def _add_hdd_attribute(self):
        self.hdd_attribute = self.env["product.attribute"].create(
            {"name": "HDD", "sequence": 3}
        )
        self.hdd_1 = self.env["product.attribute.value"].create(
            {"name": "1 To", "attribute_id": self.hdd_attribute.id, "sequence": 1}
        )
        self.hdd_2 = self.env["product.attribute.value"].create(
            {"name": "2 To", "attribute_id": self.hdd_attribute.id, "sequence": 2}
        )

        self.computer_hdd_attribute_lines = self.env[
            "product.template.attribute.line"
        ].create(
            {
                "product_tmpl_id": self.computer.id,
                "attribute_id": self.hdd_attribute.id,
                "value_ids": [(6, 0, [self.hdd_1.id, self.hdd_2.id])],
                "sequence": 1,
            }
        )

    def test_get_combination_name(self):
        variant_names = [
            variant.product_template_attribute_value_ids._get_combination_name()
            for variant in self.env["product.product"].search(
                [("product_tmpl_id", "=", self.computer.id)]
            )
        ]

        self.assertIn(
            "1 To, Mem: 256 GB, RAM: 8 GB",
            variant_names,
            "Variant name extension not found",
        )
        self.assertIn(
            "2 To, Mem: 512 GB, RAM: 16 GB",
            variant_names,
            "Variant name extension not found",
        )
        self.assertNotIn(
            "1 To, 256 GB, 8 GB", variant_names, "Variant name extension not correct"
        )
        self.assertNotIn(
            "Mem: 256 GB, 1 To, RAM: 8 GB",
            variant_names,
            "Variant name extension not correct",
        )
