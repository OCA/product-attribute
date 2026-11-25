# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductAttributeGroupByFilter(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.attr_size = cls.env["product.attribute"].create(
            {"name": "Size", "sequence": 1}
        )
        cls.val_s = cls.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": cls.attr_size.id, "sequence": 10}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.attr_size.id, "sequence": 20}
        )
        cls.val_l = cls.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": cls.attr_size.id, "sequence": 30}
        )

        cls.attr_color = cls.env["product.attribute"].create(
            {"name": "Color", "sequence": 2}
        )
        cls.val_red = cls.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": cls.attr_color.id, "sequence": 10}
        )
        cls.val_blue = cls.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": cls.attr_color.id, "sequence": 20}
        )

        cls.attr_excluded = cls.env["product.attribute"].create(
            {"name": "Excluded", "exclude_from_groupby": True}
        )

        cls.template = cls.env["product.template"].create(
            {
                "name": "Test T-Shirt",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [
                                (4, cls.val_s.id),
                                (4, cls.val_m.id),
                                (4, cls.val_l.id),
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_color.id,
                            "value_ids": [
                                (4, cls.val_red.id),
                                (4, cls.val_blue.id),
                            ],
                        },
                    ),
                ],
            }
        )
        cls.env.company.product_groupby_attribute_sort = "sequence"

    def _groupby(self, attr, slot=1, domain=None):
        return (
            self.env["product.product"]
            .with_context(**{"groupby_attribute_id_%d" % slot: attr.id})
            .read_group(
                domain=domain or [("product_tmpl_id", "=", self.template.id)],
                fields=["id"],
                groupby=["attribute_group_by_%d" % slot],
            )
        )

    def _drilldown(self, group):
        return (
            self.env["product.product"]
            .with_context(**group["__context"])
            .read_group(
                domain=group["__domain"],
                fields=["id"],
                groupby=group["__context"]["group_by"],
            )
        )

    def test_get_groupby_attribute_fields(self):
        result = self.env["product.product"].get_groupby_attribute_fields()
        ids = [product["id"] for product in result]
        self.assertIn(self.attr_size.id, ids)
        self.assertIn(self.attr_color.id, ids)
        self.assertNotIn(self.attr_excluded.id, ids)

    def test_read_group_returns_correct_values(self):
        names = [
            group["attribute_group_by_1"][1] for group in self._groupby(self.attr_size)
        ]
        self.assertIn("S", names)
        self.assertIn("M", names)
        self.assertIn("L", names)

    def test_read_group_group_structure(self):
        for group in self._groupby(self.attr_size):
            self.assertIn("attribute_group_by_1", group)
            self.assertIn("attribute_group_by_1_count", group)
            self.assertIn("__domain", group)
            self.assertIn("__context", group)
            self.assertIn("__fold", group)

    def test_read_group_domain_matches_count(self):
        for group in self._groupby(self.attr_size):
            count = self.env["product.product"].search_count(group["__domain"])
            self.assertEqual(count, group["attribute_group_by_1_count"])

    def test_read_group_without_slot(self):
        result = self.env["product.product"].read_group(
            domain=[], fields=["id"], groupby=["categ_id"]
        )
        for group in result:
            self.assertNotIn("attribute_group_by_1", group)

    def test_read_group_undefined_value(self):
        tmpl = self.env["product.template"].create({"name": "No Attr Product"})
        result = self._groupby(
            self.attr_size,
            domain=[("product_tmpl_id", "in", [self.template.id, tmpl.id])],
        )
        names = [group["attribute_group_by_1"][1] for group in result]
        self.assertIn("Undefined", names)

    def test_read_group_two_attributes(self):
        ctx = {
            "groupby_attribute_id_1": self.attr_size.id,
            "groupby_attribute_id_2": self.attr_color.id,
        }
        domain = [("product_tmpl_id", "=", self.template.id)]

        level1 = (
            self.env["product.product"]
            .with_context(**ctx)
            .read_group(
                domain=domain,
                fields=["id"],
                groupby=["attribute_group_by_1", "attribute_group_by_2"],
            )
        )
        self.assertEqual(
            {g["attribute_group_by_1"][1] for g in level1}, {"S", "M", "L"}
        )

        combinations = set()
        for g1 in level1:
            level2 = (
                self.env["product.product"]
                .with_context(**g1["__context"])
                .read_group(
                    domain=g1["__domain"],
                    fields=["id"],
                    groupby=g1["__context"]["group_by"],
                )
            )
            for g2 in level2:
                combinations.add(
                    (g1["attribute_group_by_1"][1], g2["attribute_group_by_2"][1])
                )

        self.assertEqual(
            combinations,
            {
                ("S", "Red"),
                ("S", "Blue"),
                ("M", "Red"),
                ("M", "Blue"),
                ("L", "Red"),
                ("L", "Blue"),
            },
        )

    def test_sort_by_sequence(self):
        self.env.company.product_groupby_attribute_sort = "sequence"
        names = [
            group["attribute_group_by_1"][1] for group in self._groupby(self.attr_size)
        ]
        self.assertEqual(names, ["S", "M", "L"])

    def test_sort_by_name(self):
        self.env.company.product_groupby_attribute_sort = "name"
        names = [
            group["attribute_group_by_1"][1] for group in self._groupby(self.attr_size)
        ]
        self.assertEqual(names, sorted(names))

    def test_native_then_attribute(self):
        level1 = (
            self.env["product.product"]
            .with_context(groupby_attribute_id_1=self.attr_size.id)
            .read_group(
                domain=[("product_tmpl_id", "=", self.template.id)],
                fields=["id"],
                groupby=["categ_id", "attribute_group_by_1"],
            )
        )
        for group in level1:
            self.assertNotIn("attribute_group_by_1", group)
            self.assertIn("groupby_attribute_id_1", group.get("__context", {}))

        level2 = self._drilldown(level1[0])
        names = [
            g["attribute_group_by_1"][1]
            for g in level2
            if g.get("attribute_group_by_1")
        ]
        self.assertTrue(len(names) > 0)

    def test_attribute_then_native_then_attribute(self):
        ctx = {
            "groupby_attribute_id_1": self.attr_size.id,
            "groupby_attribute_id_2": self.attr_color.id,
        }
        level1 = (
            self.env["product.product"]
            .with_context(**ctx)
            .read_group(
                domain=[("product_tmpl_id", "=", self.template.id)],
                fields=["id"],
                groupby=["attribute_group_by_1", "categ_id", "attribute_group_by_2"],
            )
        )
        self.assertEqual(
            {g["attribute_group_by_1"][1] for g in level1}, {"S", "M", "L"}
        )

        s_group = next(g for g in level1 if g["attribute_group_by_1"][1] == "S")
        level2 = self._drilldown(s_group)
        for group in level2:
            self.assertIn("groupby_attribute_id_2", group.get("__context", {}))

        level3 = self._drilldown(level2[0])
        names = [
            g["attribute_group_by_2"][1]
            for g in level3
            if g.get("attribute_group_by_2")
        ]
        self.assertIn("Red", names)
        self.assertIn("Blue", names)

    def test_domain_count_consistency_with_native_filter(self):
        level1 = (
            self.env["product.product"]
            .with_context(groupby_attribute_id_1=self.attr_size.id)
            .read_group(
                domain=[("product_tmpl_id", "=", self.template.id)],
                fields=["id"],
                groupby=["categ_id", "attribute_group_by_1"],
            )
        )
        level2 = self._drilldown(level1[0])
        for group in level2:
            count = self.env["product.product"].search_count(group["__domain"])
            self.assertEqual(count, group["attribute_group_by_1_count"])

    def test_favourite_context_persistence(self):
        level1 = self._groupby(self.attr_size)
        for group in level1:
            self.assertEqual(
                group["__context"].get("groupby_attribute_id_1"),
                self.attr_size.id,
            )
