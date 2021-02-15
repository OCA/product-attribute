# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class ABCClassificationCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(ABCClassificationCase, cls).setUpClass()
        # add a fake profile_type
        cls.ABCClassificationProfile = cls.env["abc.classification.profile"]
        cls.ABCClassificationProfile._fields["profile_type"].selection = [
            ("test_type", "Test Type")
        ]
        cls.classification_profile = cls.ABCClassificationProfile.create(
            {"name": "Profile test", "profile_type": "test_type"}
        )


class ABCClassificationLevelCase(ABCClassificationCase):
    @classmethod
    def setUpClass(cls):
        super(ABCClassificationLevelCase, cls).setUpClass()
        cls.classification_profile.write(
            {
                "level_ids": [
                    (
                        0,
                        0,
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "a",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "b",
                        },
                    ),
                ]
            }
        )

        levels = cls.classification_profile.level_ids
        cls.classification_level_a = levels.filtered(lambda l: l.name == "a")
        cls.classification_level_b = levels.filtered(lambda l: l.name == "b")
        cls.classification_profile_bis = cls.ABCClassificationProfile.create(
            {
                "name": "Profile test bis",
                "profile_type": "test_type",
                "level_ids": [
                    (
                        0,
                        0,
                        {
                            "percentage": 80,
                            "percentage_products": 40,
                            "name": "a",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "percentage": 20,
                            "percentage_products": 60,
                            "name": "b",
                        },
                    ),
                ],
            }
        )
        levels = cls.classification_profile_bis.level_ids
        cls.classification_level_bis_a = levels.filtered(
            lambda l: l.name == "a"
        )

        # create a template with one variant adn declare attributes to create
        # an other variant on demand
        cls.size_attr = cls.env["product.attribute"].create(
            {
                "name": "Size",
                "create_variant": False,
                "value_ids": [(0, 0, {"name": "S"}), (0, 0, {"name": "M"})],
            }
        )
        cls.size_attr_value_s = cls.size_attr.value_ids[0]
        cls.size_attr_value_m = cls.size_attr.value_ids[1]
        cls.uom_unit = cls.env.ref("product.product_uom_unit")
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test sized",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.size_attr.id,
                            "value_ids": [(6, 0, cls.size_attr.value_ids.ids)],
                        },
                    )
                ],
            }
        )
        cls.product_product = cls.product_template.product_variant_ids
        cls.ProductLevel = cls.env["abc.classification.product.level"]

    @classmethod
    def _create_variant(cls, size_value):
        return cls.env["product.product"].create(
            {
                "product_tmpl_id": cls.product_template.id,
                "attribute_value_ids": [(6, 0, size_value.ids)],
            }
        )
