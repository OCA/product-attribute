# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.base.tests.common import BaseCommon


class TestProductAttributeValueSortAlphabetical(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {
                "name": "Size",
                "value_ids": [
                    (0, 0, {"name": "Medium", "sequence": 1}),
                    (0, 0, {"name": "large", "sequence": 2}),
                    (0, 0, {"name": "Small", "sequence": 3}),
                ],
            }
        )

    def _get_names(self):
        self.env.invalidate_all()
        return self.attribute.value_ids.sorted("sequence").mapped("name")

    def test_default_manual_sort(self):
        self.assertFalse(self.attribute.sort_alphabetically)
        self.assertEqual(self.attribute.sort_field, "name")
        self.assertEqual(self._get_names(), ["Medium", "large", "Small"])

    def test_enable_alphabetical_sort(self):
        self.attribute.sort_alphabetically = True
        self.assertEqual(self._get_names(), ["large", "Medium", "Small"])

    def test_add_value(self):
        self.attribute.sort_alphabetically = True
        self.env["product.attribute.value"].create(
            {"name": "Extra Large", "attribute_id": self.attribute.id}
        )
        self.assertEqual(self._get_names(), ["Extra Large", "large", "Medium", "Small"])

    def test_rename_value(self):
        self.attribute.sort_alphabetically = True
        small = self.attribute.value_ids.filtered(lambda v: v.name == "Small")
        small.name = "Akward"
        self.assertEqual(self._get_names(), ["Akward", "large", "Medium"])

    def test_disable_keeps_sequence(self):
        self.attribute.sort_alphabetically = True
        self.assertEqual(self._get_names(), ["large", "Medium", "Small"])
        self.attribute.sort_alphabetically = False
        self.attribute.value_ids.filtered(lambda v: v.name == "Medium").sequence = 0
        self.assertEqual(self._get_names(), ["Medium", "large", "Small"])
