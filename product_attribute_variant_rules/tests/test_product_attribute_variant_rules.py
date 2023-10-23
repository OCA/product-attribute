from odoo.addons.product.tests.test_product_attribute_value_config import (
    TestProductAttributeValueCommon,
)


class TestProductAttributeVariantRules(TestProductAttributeValueCommon):
    def _expand_variants_attributes(self, product_template):
        return {
            self._expand_variant_attributes(variant)
            for variant in product_template._get_possible_variants()
        }

    def _expand_variant_attributes(self, variant):
        return tuple(variant.product_template_attribute_value_ids.mapped("name"))

    def test_product_attribute_no_rules_variants(self):
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "1 To"),
                ("256 GB", "16 GB", "2 To"),
                ("256 GB", "16 GB", "4 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "2 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "1 To"),
                ("512 GB", "16 GB", "2 To"),
                ("512 GB", "16 GB", "4 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "2 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_inactive_rules_variants(self):
        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(4, self.ram_16.id)],
                    "rule_type": "only",
                    "product_attribute_value_postcondition_ids": [(4, self.hdd_1.id)],
                },
            )
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "1 To"),
                ("256 GB", "16 GB", "2 To"),
                ("256 GB", "16 GB", "4 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "2 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "1 To"),
                ("512 GB", "16 GB", "2 To"),
                ("512 GB", "16 GB", "4 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "2 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_rule_simple_only_rule(self):
        self.computer.use_attribute_rules = True
        # Remove all variants that have 16GB RAM and not 1To HDD
        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(4, self.ram_16.id)],
                    "rule_type": "only",
                    "product_attribute_value_postcondition_ids": [(4, self.hdd_1.id)],
                },
            )
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "1 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "2 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "1 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "2 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_rule_simple_never_rule(self):
        self.computer.use_attribute_rules = True
        # Remove all variants that have 16GB RAM and 1To HDD
        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(4, self.ram_16.id)],
                    "rule_type": "never",
                    "product_attribute_value_postcondition_ids": [(4, self.hdd_1.id)],
                },
            )
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "2 To"),
                ("256 GB", "16 GB", "4 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "2 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "2 To"),
                ("512 GB", "16 GB", "4 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "2 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_rule_complex(self):
        self.computer.use_attribute_rules = True
        # Remove all variants that have (8GB or 32GB RAM and 2To HDD) and not 256GB SSD
        # Remove all variants that have (16GB RAM) and not ((2To or 4To HDD) and 512GB SSD)
        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [
                        (4, self.ram_8.id),
                        (4, self.ram_32.id),
                        (4, self.hdd_2.id),
                    ],
                    "rule_type": "only",
                    "product_attribute_value_postcondition_ids": [(4, self.ssd_256.id)],
                },
            ),
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(4, self.ram_16.id)],
                    "rule_type": "never",
                    "product_attribute_value_postcondition_ids": [
                        (4, self.hdd_4.id),
                        (4, self.ssd_512.id),
                        (4, self.hdd_2.id),
                    ],
                },
            ),
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "1 To"),
                ("256 GB", "16 GB", "2 To"),
                ("256 GB", "16 GB", "4 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "2 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "1 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_rule_no_precondition_only(self):
        self.computer.use_attribute_rules = True
        # Remove all variants that have not (256GB SSD and 8GB or 32GB RAM and 2To HDD)

        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(5,)],
                    "rule_type": "only",
                    "product_attribute_value_postcondition_ids": [
                        (4, self.ssd_256.id),
                        (4, self.ram_8.id),
                        (4, self.ram_32.id),
                        (4, self.hdd_2.id),
                    ],
                },
            ),
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "2 To"),
                ("256 GB", "32 GB", "2 To"),
            },
        )

    def test_product_attribute_rule_no_precondition_never(self):
        self.computer.use_attribute_rules = True
        # Remove all variants that have (256GB SSD and 8GB or 32GB RAM and 2To HDD)

        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(5,)],
                    "rule_type": "never",
                    "product_attribute_value_postcondition_ids": [
                        (4, self.ssd_256.id),
                        (4, self.ram_8.id),
                        (4, self.ram_32.id),
                        (4, self.hdd_2.id),
                    ],
                },
            ),
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
                ("256 GB", "8 GB", "4 To"),
                ("256 GB", "16 GB", "1 To"),
                ("256 GB", "16 GB", "2 To"),
                ("256 GB", "16 GB", "4 To"),
                ("256 GB", "32 GB", "1 To"),
                ("256 GB", "32 GB", "4 To"),
                ("512 GB", "8 GB", "1 To"),
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "8 GB", "4 To"),
                ("512 GB", "16 GB", "1 To"),
                ("512 GB", "16 GB", "2 To"),
                ("512 GB", "16 GB", "4 To"),
                ("512 GB", "32 GB", "1 To"),
                ("512 GB", "32 GB", "2 To"),
                ("512 GB", "32 GB", "4 To"),
            },
        )

    def test_product_attribute_rule_no_precondition_both(self):
        self.computer.use_attribute_rules = True

        self.computer.product_attribute_rule_ids = [
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(5,)],
                    "rule_type": "never",
                    "product_attribute_value_postcondition_ids": [
                        (4, self.ssd_256.id),
                        (4, self.ram_8.id),
                        (4, self.ram_32.id),
                        (4, self.hdd_2.id),
                    ],
                },
            ),
            (
                0,
                0,
                {
                    "product_tmpl_id": self.computer.id,
                    "product_attribute_value_precondition_ids": [(5,)],
                    "rule_type": "only",
                    "product_attribute_value_postcondition_ids": [
                        (4, self.ssd_256.id),
                        (4, self.ram_8.id),
                        (4, self.hdd_1.id),
                        (4, self.hdd_2.id),
                    ],
                },
            ),
        ]
        self.assertEqual(
            self._expand_variants_attributes(self.computer),
            {
                ("256 GB", "8 GB", "1 To"),
            },
        )
