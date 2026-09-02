# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class CommonProductPricelistAlternative(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.datacard = cls.env["product.product"].create(
            {"name": "Data card", "list_price": 100}
        )
        cls.usb_adapter = cls.env["product.product"].create(
            {"name": "Usb adapter", "list_price": 100}
        )
        cls.color_attribute = cls.env["product.attribute"].create(
            {"name": "Color", "create_variant": "always"}
        )
        cls.black_attribute_value = cls.env["product.attribute.value"].create(
            {"name": "Black", "attribute_id": cls.color_attribute.id}
        )
        cls.yellow_attribute_value = cls.env["product.attribute.value"].create(
            {"name": "Yellow", "attribute_id": cls.color_attribute.id}
        )
        cls.configurable_product_template = cls.env["product.template"].create(
            {
                "name": "Configurable gloves",
                "list_price": 100,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.color_attribute.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        cls.black_attribute_value.id,
                                        cls.yellow_attribute_value.id,
                                    ]
                                )
                            ],
                        }
                    )
                ],
            }
        )
        attribute_lines = cls.configurable_product_template.attribute_line_ids
        template_values = attribute_lines.product_template_value_ids
        cls.yellow_combination = template_values.filtered(
            lambda ptav: ptav.product_attribute_value_id == cls.yellow_attribute_value
        )
        cls.yellow_gloves = (
            cls.configurable_product_template._get_variant_for_combination(
                cls.yellow_combination
            )
        )

        cls.alternative_pricelist_01 = cls.env["product.pricelist"].create(
            {
                "name": "Alternative pricelist 01",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.usb_adapter.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                ],
            }
        )
        cls.alternative_pricelist_02 = cls.env["product.pricelist"].create(
            {
                "name": "Alternative pricelist 02",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.datacard.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 80,
                        }
                    ),
                ],
            }
        )
        cls.alternative_pricelist_03 = cls.env["product.pricelist"].create(
            {
                "name": "Alternative pricelist 03",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.usb_adapter.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 110,
                        }
                    ),
                ],
            }
        )

        cls.pricelist01 = cls.env["product.pricelist"].create(
            {
                "name": "Sale pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.usb_adapter.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 95,
                        }
                    ),
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.datacard.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    (4, cls.alternative_pricelist_01.id),
                    (4, cls.alternative_pricelist_02.id),
                ],
            }
        )
        cls.pricelist03 = cls.env["product.pricelist"].create(
            {
                "name": "Sale pricelist based on another pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.pricelist01.id,
                            "applied_on": "3_global",
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    Command.link(cls.alternative_pricelist_03.id),
                ],
            }
        )

        cls.product_categ01 = cls.env["product.category"].create(
            {"name": "Category 01"}
        )
        cls.usb_adapter.categ_id = cls.product_categ01

        cls.pricelist02 = cls.env["product.pricelist"].create(
            {
                "name": "Sale pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "percentage",
                            "applied_on": "2_product_category",
                            "categ_id": cls.product_categ01.id,
                            "percent_price": 40,
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    (4, cls.alternative_pricelist_01.id),
                ],
            }
        )
        cls.alternative_promotion_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Alternative promotion pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.yellow_gloves.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 41.5,
                        }
                    ),
                ],
            }
        )
        cls.configurable_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Configurable product pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "list_price",
                            "price_discount": -15,
                            "product_tmpl_id": cls.configurable_product_template.id,
                            "applied_on": "1_product",
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    Command.link(cls.alternative_promotion_pricelist.id),
                ],
            }
        )
