from odoo import Command

from odoo.addons.product.tests.test_product_attribute_value_config import (
    TestProductAttributeValueCommon,
)

# Variant creating attribute values of the "Super Computer" template.
SSD_VALUES = ["256 GB", "512 GB"]
RAM_VALUES = ["8 GB", "16 GB", "32 GB"]
HDD_VALUES = ["1 To", "2 To", "4 To"]

# All the combinations of the template (2 * 3 * 3 = 18).
ALL_VARIANTS = {
    (ssd, ram, hdd) for ssd in SSD_VALUES for ram in RAM_VALUES for hdd in HDD_VALUES
}


class TestProductAttributeVariantRules(TestProductAttributeValueCommon):
    def _get_variants(self, product_template):
        """Return the active variants as a set of (ssd, ram, hdd) tuples."""
        return {
            tuple(variant.product_template_attribute_value_ids.mapped("name"))
            for variant in product_template.product_variant_ids
        }

    def _rule(self, rule_type, postconditions, preconditions=None):
        """Build the create command of a product.attribute.rule.

        Different attributes of a same group of conditions are ANDed while
        values of a same attribute are ORed.
        """
        return Command.create(
            {
                "product_attribute_value_precondition_ids": [
                    Command.set([value.id for value in preconditions or []])
                ],
                "rule_type": rule_type,
                "product_attribute_value_postcondition_ids": [
                    Command.set([value.id for value in postconditions])
                ],
            }
        )

    def test_product_attribute_no_rules_variants(self):
        """Without rule, all the combinations are generated."""
        self.assertEqual(self._get_variants(self.computer), ALL_VARIANTS)

    def test_product_attribute_inactive_rules_variants(self):
        """Rules don't affect the variants as long as they are not enabled."""
        self.assertFalse(self.computer.use_attribute_rules)
        self.computer.product_attribute_rule_ids = [
            self._rule("only", preconditions=[self.ram_16], postconditions=[self.hdd_1])
        ]
        self.assertEqual(self._get_variants(self.computer), ALL_VARIANTS)

    def test_product_attribute_rule_simple_only_rule(self):
        """16GB RAM is only available with 1To HDD."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            self._rule("only", preconditions=[self.ram_16], postconditions=[self.hdd_1])
        ]
        self.assertEqual(
            self._get_variants(self.computer),
            ALL_VARIANTS
            - {(ssd, "16 GB", hdd) for ssd in SSD_VALUES for hdd in ["2 To", "4 To"]},
        )

    def test_product_attribute_rule_simple_never_rule(self):
        """16GB RAM is never available with 1To HDD."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            self._rule(
                "never", preconditions=[self.ram_16], postconditions=[self.hdd_1]
            )
        ]
        self.assertEqual(
            self._get_variants(self.computer),
            ALL_VARIANTS - {(ssd, "16 GB", "1 To") for ssd in SSD_VALUES},
        )

    def test_product_attribute_rule_complex(self):
        """Rules with several attributes and values."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            # (8GB or 32GB RAM and 2To HDD) is only available with 256GB SSD.
            self._rule(
                "only",
                preconditions=[self.ram_8, self.ram_32, self.hdd_2],
                postconditions=[self.ssd_256],
            ),
            # 16GB RAM is never available with 512GB SSD and (2To or 4To HDD).
            self._rule(
                "never",
                preconditions=[self.ram_16],
                postconditions=[self.hdd_4, self.ssd_512, self.hdd_2],
            ),
        ]
        self.assertEqual(
            self._get_variants(self.computer),
            ALL_VARIANTS
            - {
                ("512 GB", "8 GB", "2 To"),
                ("512 GB", "16 GB", "2 To"),
                ("512 GB", "16 GB", "4 To"),
                ("512 GB", "32 GB", "2 To"),
            },
        )

    def test_product_attribute_rule_no_precondition_only(self):
        """Only the combinations matching the postconditions are kept."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            self._rule(
                "only",
                postconditions=[self.ssd_256, self.ram_8, self.ram_32, self.hdd_2],
            )
        ]
        self.assertEqual(
            self._get_variants(self.computer),
            {("256 GB", "8 GB", "2 To"), ("256 GB", "32 GB", "2 To")},
        )

    def test_product_attribute_rule_no_precondition_never(self):
        """The combinations matching the postconditions are removed."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            self._rule(
                "never",
                postconditions=[self.ssd_256, self.ram_8, self.ram_32, self.hdd_2],
            )
        ]
        self.assertEqual(
            self._get_variants(self.computer),
            ALL_VARIANTS - {("256 GB", "8 GB", "2 To"), ("256 GB", "32 GB", "2 To")},
        )

    def test_product_attribute_rule_no_precondition_both(self):
        """Rules without precondition are combined together."""
        self.computer.use_attribute_rules = True
        self.computer.product_attribute_rule_ids = [
            self._rule(
                "never",
                postconditions=[self.ssd_256, self.ram_8, self.ram_32, self.hdd_2],
            ),
            self._rule(
                "only",
                postconditions=[self.ssd_256, self.ram_8, self.hdd_1, self.hdd_2],
            ),
        ]
        self.assertEqual(
            self._get_variants(self.computer), {("256 GB", "8 GB", "1 To")}
        )

    def test_product_attribute_rule_available_attributes(self):
        """The attribute lists used by the view fields and domains."""
        self.computer.product_attribute_rule_ids = [
            self._rule("only", preconditions=[self.ram_16], postconditions=[self.hdd_1])
        ]
        rule = self.computer.product_attribute_rule_ids
        template_attributes = self.computer.attribute_line_ids.attribute_id
        # An attribute used in the postconditions is not available anymore
        # as a precondition (and vice versa).
        self.assertEqual(
            rule.available_precondition_attribute_ids,
            template_attributes - self.hdd_attribute,
        )
        self.assertEqual(
            rule.available_postcondition_attribute_ids,
            template_attributes - self.ram_attribute,
        )
        # The technical field maps all the values of the template.
        self.assertEqual(
            self.computer.product_attribute_value_ids,
            self.computer.attribute_line_ids.value_ids,
        )
