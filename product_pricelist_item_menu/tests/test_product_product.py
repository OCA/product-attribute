from odoo.tests import common


class TestProductMixin(common.TransactionCase):
    def setUp(self):
        super(TestProductMixin, self).setUp()
        product_template_model = self.env["product.template"]
        ptav_model = self.env["product.template.attribute.value"]
        product_attribute_model = self.env["product.attribute"]
        product_attribute_value_model = self.env["product.attribute.value"]
        product_template_attribute_line_model = self.env[
            "product.template.attribute.line"
        ]
        product_template_attribute_value_model = self.env[
            "product.template.attribute.value"
        ]
        ooops_dimension_exclusion_rule_model = self.env[
            "ooops.dimension.exclusion.rule"
        ]
        ooops_dimension_exclusion_rule_line_model = self.env[
            "ooops.dimension.exclusion.rule.line"
        ]

        self.product_attribute_length = product_attribute_model.create(
            {
                "name": "Length",
                "display_type": "radio",
                "create_variant": "no_variant",
                "dimension": "product_height",
            }
        )
        self.product_attribute_value_length_mm = product_attribute_value_model.create(
            {
                "name": "mm",
                "is_custom": True,
                "attribute_id": self.product_attribute_length.id,
                "uom_id": self.env.ref(
                    "product_pricelist_items_menu.product_uom_mm"
                ).id,
            }
        )
        self.product_attribute_width = product_attribute_model.create(
            {
                "name": "Width",
                "display_type": "radio",
                "create_variant": "no_variant",
                "dimension": "product_width",
            }
        )
        self.product_attribute_value_width_mm = product_attribute_value_model.create(
            {
                "name": "mm",
                "is_custom": True,
                "attribute_id": self.product_attribute_width.id,
                "uom_id": self.env.ref(
                    "product_pricelist_items_menu.product_uom_mm"
                ).id,
            }
        )
        self.product_attribute_height = product_attribute_model.create(
            {
                "name": "Height",
                "display_type": "radio",
                "create_variant": "no_variant",
                "dimension": "product_height",
            }
        )
        self.product_attribute_value_height_mm = product_attribute_value_model.create(
            {
                "name": "mm",
                "is_custom": True,
                "attribute_id": self.product_attribute_height.id,
                "uom_id": self.env.ref(
                    "product_pricelist_items_menu.product_uom_mm"
                ).id,
            }
        )

        self.product_template_test_product = product_template_model.create(
            {
                "name": "Test product",
                "type": "product",
                "list_price": 0.0,
            }
        )
        self.product_template_test_product._create_variant_ids()

        self.product_template_attribute_line_length = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product.id,
                    "attribute_id": self.product_attribute_length.id,
                    "value_ids": [(4, self.product_attribute_value_length_mm.id)],
                }
            )
        )
        self.product_template_attribute_line_width = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product.id,
                    "attribute_id": self.product_attribute_width.id,
                    "value_ids": [(4, self.product_attribute_value_width_mm.id)],
                }
            )
        )
        self.product_template_attribute_line_height = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product.id,
                    "attribute_id": self.product_attribute_height.id,
                    "value_ids": [(4, self.product_attribute_value_height_mm.id)],
                }
            )
        )

        self.ptav_lenght_mm = product_template_attribute_value_model.search(
            [
                ("product_tmpl_id", "=", self.product_template_test_product.id),
                ("attribute_id", "=", self.product_attribute_length.id),
                (
                    "product_attribute_value_id",
                    "=",
                    self.product_attribute_value_length_mm.id,
                ),
            ]
        )
        self.ptav_width_mm = product_template_attribute_value_model.search(
            [
                ("product_tmpl_id", "=", self.product_template_test_product.id),
                ("attribute_id", "=", self.product_attribute_width.id),
                (
                    "product_attribute_value_id",
                    "=",
                    self.product_attribute_value_width_mm.id,
                ),
            ]
        )
        self.ptav_height_mm = product_template_attribute_value_model.search(
            [
                ("product_tmpl_id", "=", self.product_template_test_product.id),
                ("attribute_id", "=", self.product_attribute_height.id),
                (
                    "product_attribute_value_id",
                    "=",
                    self.product_attribute_value_height_mm.id,
                ),
            ]
        )

        self.combination = ptav_model.browse(
            [
                self.ptav_lenght_mm.id,
                self.ptav_width_mm.id,
                self.ptav_height_mm.id,
            ]
        )

        self.product_template_test_product_with_der = product_template_model.create(
            {
                "name": "Test product with der",
                "type": "product",
                "list_price": 0.0,
            }
        )

        self.product_template_test_product_with_der_attribute_line_length = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product_with_der.id,
                    "attribute_id": self.product_attribute_length.id,
                    "value_ids": [(4, self.product_attribute_value_length_mm.id)],
                }
            )
        )
        self.product_template_test_product_with_der_attribute_line_width = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product_with_der.id,
                    "attribute_id": self.product_attribute_width.id,
                    "value_ids": [(4, self.product_attribute_value_width_mm.id)],
                }
            )
        )
        self.product_template_test_product_with_der_attribute_line_height = (
            product_template_attribute_line_model.create(
                {
                    "product_tmpl_id": self.product_template_test_product_with_der.id,
                    "attribute_id": self.product_attribute_height.id,
                    "value_ids": [(4, self.product_attribute_value_height_mm.id)],
                }
            )
        )

        self.ptav_test_product_with_der_lenght_mm = (
            product_template_attribute_value_model.search(
                [
                    (
                        "product_tmpl_id",
                        "=",
                        self.product_template_test_product_with_der.id,
                    ),
                    ("attribute_id", "=", self.product_attribute_length.id),
                    (
                        "product_attribute_value_id",
                        "=",
                        self.product_attribute_value_length_mm.id,
                    ),
                ]
            )
        )
        self.ptav_test_product_with_der_width_mm = (
            product_template_attribute_value_model.search(
                [
                    (
                        "product_tmpl_id",
                        "=",
                        self.product_template_test_product_with_der.id,
                    ),
                    ("attribute_id", "=", self.product_attribute_width.id),
                    (
                        "product_attribute_value_id",
                        "=",
                        self.product_attribute_value_width_mm.id,
                    ),
                ]
            )
        )
        self.ptav_test_product_with_der_height_mm = (
            product_template_attribute_value_model.search(
                [
                    (
                        "product_tmpl_id",
                        "=",
                        self.product_template_test_product_with_der.id,
                    ),
                    ("attribute_id", "=", self.product_attribute_height.id),
                    (
                        "product_attribute_value_id",
                        "=",
                        self.product_attribute_value_height_mm.id,
                    ),
                ]
            )
        )

        self.combination_test_product_with_der = ptav_model.browse(
            [
                self.ptav_test_product_with_der_lenght_mm.id,
                self.ptav_test_product_with_der_width_mm.id,
                self.ptav_test_product_with_der_height_mm.id,
            ]
        )

        self.ooops_dimension_exclusion_rule_line_length = (
            ooops_dimension_exclusion_rule_line_model.create(
                {
                    "dimension": "product_height",
                    "value_from": 10.0,
                    "value_to": 125.0,
                }
            )
        )
        self.ooops_dimension_exclusion_rule_line_width = (
            ooops_dimension_exclusion_rule_line_model.create(
                {
                    "dimension": "product_width",
                    "value_from": 10.0,
                    "value_to": 125.0,
                }
            )
        )

        self.ooops_dimension_exclusion_rule_line_height = (
            ooops_dimension_exclusion_rule_line_model.create(
                {
                    "dimension": "product_height",
                    "value_from": 10.0,
                    "value_to": 125.0,
                }
            )
        )

        self.ooops_dimension_exclusion_rule_der_one = (
            ooops_dimension_exclusion_rule_model.create(
                {
                    "name": "Der one",
                    "value_ids": [(4, self.product_attribute_value_length_mm.id)],
                    "line_ids": [
                        (4, self.ooops_dimension_exclusion_rule_line_length.id)
                    ],
                    "product_tmpl_ids": [
                        (6, 0, [self.product_template_test_product_with_der.id])
                    ],
                }
            )
        )

    # Test Product Template model methods
    def test_is_combination_possible(self):
        combination_is_possible = self.product_template_test_product.with_context(
            product_height=100,
        )._is_combination_possible(self.combination)
        self.assertIs(
            combination_is_possible,
            True,
            msg="""
            The calculation of the correct combination is wrong.
            This combination must be possible
            """,
        )

    def test_is_combination_possible_with_der(self):
        combination_is_possible = (
            self.product_template_test_product_with_der.with_context(
                product_height=100,
            )._is_combination_possible(self.combination_test_product_with_der)
        )
        self.assertIs(
            combination_is_possible,
            False,
            msg="""
            The calculation of the correct combination is wrong.
            This combination must be impossible
            """,
        )

    def test_get_attribute_exclusions(self):
        attribute_exclusions = (
            self.product_template_test_product_with_der._get_attribute_exclusions()
        )
        dimensions_exclusions = attribute_exclusions["dimensions_exclusions"]
        self.assertIn(
            [
                {
                    self.ooops_dimension_exclusion_rule_line_length.dimension: [
                        self.ooops_dimension_exclusion_rule_line_length.value_from,
                        self.ooops_dimension_exclusion_rule_line_length.value_to,
                    ]
                }
            ],
            dimensions_exclusions.values(),
            msg="""
                Dimension exclusion rule must be in dimensions_exclusions keys
            """,
        )
