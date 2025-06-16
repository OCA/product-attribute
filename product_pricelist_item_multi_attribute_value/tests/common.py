# Copyright 2025 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class CommonPricelistPerMultiAttributeValue(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.legs_attribute = cls.env.ref("product.product_attribute_1")
        cls.legs_att_value_steel = cls.env.ref("product.product_attribute_value_1")
        cls.legs_att_value_alu = cls.env.ref("product.product_attribute_value_2")
        cls.color_attribute = cls.env.ref("product.product_attribute_2")
        cls.color_att_value_white = cls.env.ref("product.product_attribute_value_3")
        cls.color_att_value_black = cls.env.ref("product.product_attribute_value_4")

        cls.pricelist = cls.env["product.pricelist"].create({"name": "Test Pricelist"})

        cls.template = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "list_price": 100,
                "categ_id": cls.env.ref("product.product_category_1").id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.legs_attribute.id,
                            "value_ids": [
                                cls.legs_att_value_steel.id,
                                cls.legs_att_value_alu.id,
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.color_attribute.id,
                            "value_ids": [
                                cls.color_att_value_white.id,
                                cls.color_att_value_black.id,
                            ],
                        },
                    ),
                ],
            }
        )

        cls.template._create_variant_ids()

        def find_variant(attr_values):
            return cls.template.product_variant_ids.filtered(
                lambda p: set(
                    p.product_template_attribute_value_ids.mapped(
                        "product_attribute_value_id"
                    ).ids
                )
                == set(attr_values)
            )

        cls.product_steel_white = find_variant(
            [cls.legs_att_value_steel.id, cls.color_att_value_white.id]
        )
        cls.product_alu_black = find_variant(
            [cls.legs_att_value_alu.id, cls.color_att_value_black.id]
        )
        cls.product_alu_white = find_variant(
            [cls.legs_att_value_alu.id, cls.color_att_value_white.id]
        )

        cls.pricelist_item = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist.id,
                "product_tmpl_id": cls.template.id,
                "base": "list_price",
                "fixed_price": 100,
            }
        )

        cls.color_price = cls.env["product.pricelist.item.attribute.value"].create(
            {
                "pricelist_item_id": cls.pricelist_item.id,
                "attribute_value_ids": [
                    (6, 0, [cls.color_att_value_black.id, cls.color_att_value_white.id])
                ],
                "additional_price": 50,
            }
        )

        cls.legs_price = cls.env["product.pricelist.item.attribute.value"].create(
            {
                "pricelist_item_id": cls.pricelist_item.id,
                "attribute_value_ids": [(6, 0, [cls.legs_att_value_alu.id])],
                "additional_price": 25,
            }
        )

        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.env.ref("base.res_partner_1").id,
                "pricelist_id": cls.pricelist.id,
            }
        )

    def new_sale_line(self, product):
        return self.env["sale.order.line"].create(
            {
                "order_id": self.sale.id,
                "product_id": product.id,
                "product_uom_qty": 1,
                "product_uom": product.uom_id.id,
            }
        )
