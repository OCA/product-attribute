# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class ABCClassificationCase(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # add a fake profile_type
        cls.ABCClassificationProfile = cls.env["abc.classification.profile"]
        cls._patch_profile_type_selection([("test_type", "Test Type")])
        cls.classification_profile = cls.ABCClassificationProfile.create(
            {"name": "Profile test", "profile_type": "test_type"}
        )

    @classmethod
    def _patch_profile_type_selection(cls, selection):
        """Register a fake profile type on the registry field.

        The field is shared by the whole registry, so the original values are
        restored once the test class is done.
        """
        field = cls.ABCClassificationProfile._fields["profile_type"]
        original_selection = field.selection
        original_values = field._selection
        field.selection = selection
        field._selection = dict(selection)

        def _restore():
            field.selection = original_selection
            field._selection = original_values

        cls.addClassCleanup(_restore)


class ABCClassificationLevelCase(ABCClassificationCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.classification_profile.write(
            {
                "level_ids": [
                    Command.create(
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "a",
                        }
                    ),
                    Command.create(
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "b",
                        }
                    ),
                ]
            }
        )

        levels = cls.classification_profile.level_ids
        cls.classification_level_a = levels.filtered(lambda level: level.name == "a")
        cls.classification_level_b = levels.filtered(lambda level: level.name == "b")
        cls.classification_profile_bis = cls.ABCClassificationProfile.create(
            {
                "name": "Profile test bis",
                "profile_type": "test_type",
                "level_ids": [
                    Command.create(
                        {
                            "percentage": 80,
                            "percentage_products": 40,
                            "name": "a",
                        }
                    ),
                    Command.create(
                        {
                            "percentage": 20,
                            "percentage_products": 60,
                            "name": "b",
                        }
                    ),
                ],
            }
        )
        levels = cls.classification_profile_bis.level_ids
        cls.classification_level_bis_a = levels.filtered(
            lambda level: level.name == "a"
        )

        cls.classification_level_bis_b = levels.filtered(
            lambda level: level.name == "b"
        )
        # create a template with one variant adn declare attributes to create
        # another variant on demand
        cls.size_attr = cls.env["product.attribute"].create(
            {
                "name": "Size",
                "create_variant": "no_variant",
                "value_ids": [
                    Command.create({"name": "S"}),
                    Command.create({"name": "M"}),
                ],
            }
        )
        cls.size_attr_value_s = cls.size_attr.value_ids[0]
        cls.size_attr_value_m = cls.size_attr.value_ids[1]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_category = cls.env["product.category"].create(
            {"name": "Test ABC Classification"}
        )
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test sized",
                "categ_id": cls.product_category.id,
                "uom_id": cls.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.size_attr.id,
                            "value_ids": [Command.set(cls.size_attr.value_ids.ids)],
                        }
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
                "product_template_attribute_value_ids": [
                    Command.set(
                        size_value.pav_attribute_line_ids.product_template_value_ids.ids
                    )
                ],
            }
        )
