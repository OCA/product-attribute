# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests.common import SavepointCase


class TestAbcClassificationProfile(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAbcClassificationProfile, cls).setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {"name": "Unittest partner", "ref": "12344566777878"}
        )

        cls.warehouse_1 = cls.env.ref("stock.warehouse0")
        cls.warehouse_1.write(
            {
                "name": "Test Warehouse",
                "reception_steps": "one_step",
                "delivery_steps": "pick_ship",
                "code": "TST",
            }
        )
        cls.warehouse_1.pick_type_id.subcode = "PICK"
        cls.warehouse_1.pick_type_id.groupbypartner = False
        cls.warehouse_1.out_type_id.groupbypartner = True

        cls.level_A = cls.env["abc.classification.level"].create(
            {"name": "A", "percentage": 80}
        )

        cls.level_B = cls.env["abc.classification.level"].create(
            {"name": "B", "percentage": 15}
        )

        cls.level_C = cls.env["abc.classification.level"].create(
            {"name": "C", "percentage": 5}
        )

        cls.stock_profile = cls.env["abc.classification.profile"].create(
            {
                "name": "Stock profile",
                "profile_type": "stock",
                "period": 365,
                "level_ids": [(6, 0, [cls.level_A.id, cls.level_B.id, cls.level_C.id])],
            }
        )

        cls.product1 = cls.env["product.product"].create(
            {
                "name": "Product1",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "987654321",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Product2",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "123456789",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls.product3 = cls.env["product.product"].create(
            {
                "name": "Product3",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "67548309",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls.product4 = cls.env["product.product"].create(
            {
                "name": "Product4",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "123409876",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls.product5 = cls.env["product.product"].create(
            {
                "name": "Product5",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "0987540321",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls.product6 = cls.env["product.product"].create(
            {
                "name": "Product6",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "345789732",
                "tracking": "none",
                "abc_classification_profile_ids": [(4, cls.stock_profile.id)],
            }
        )

        cls._create_availability(cls.product1)
        cls._create_availability(cls.product2)
        cls._create_availability(cls.product3)
        cls._create_availability(cls.product4)
        cls._create_availability(cls.product5)
        cls._create_availability(cls.product6)

        cls.so1 = cls._confirm_sale_order(
            products=[cls.product1, cls.product2, cls.product3],
            qty={cls.product1.name: 80, cls.product2.name: 10, cls.product3.name: 30},
        )
        cls._confirm_pick_ship(cls.so1)

        cls.so2 = cls._confirm_sale_order(
            products=[cls.product4, cls.product5, cls.product6],
            qty={cls.product4.name: 5, cls.product5.name: 30, cls.product6.name: 25},
        )
        cls._confirm_pick_ship(cls.so2)

        cls.so3 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 75}
        )
        cls._confirm_pick_ship(cls.so3)

        cls.so3 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 75}
        )
        cls._confirm_pick_ship(cls.so3)

        cls.so4 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 25}
        )
        cls._confirm_pick_ship(cls.so4)

        cls.so5 = cls._confirm_sale_order(
            products=[cls.product3, cls.product5],
            qty={cls.product3.name: 90, cls.product5.name: 50},
        )
        cls._confirm_pick_ship(cls.so5)

        cls.so6 = cls._confirm_sale_order(
            products=[cls.product6], qty={cls.product6.name: 30}
        )
        cls._confirm_pick_ship(cls.so6)

    @classmethod
    def _create_availability(cls, product):
        update_qty_wizard = cls.env["stock.change.product.qty"].create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "new_quantity": 500,
                "location_id": cls.warehouse_1.lot_stock_id.id,
            }
        )
        update_qty_wizard.change_product_qty()

    @classmethod
    def _confirm_sale_order(cls, products, qty, partner=None):
        if partner is None:
            partner = cls.partner
        warehouse = cls.warehouse_1
        Sale = cls.env["sale.order"]
        lines = [
            (
                0,
                0,
                {
                    "name": p.name,
                    "product_id": p.id,
                    "product_uom_qty": qty[p.name],
                    "product_uom": p.uom_id.id,
                    "price_unit": 1,
                },
            )
            for p in products
        ]
        so_values = {
            "partner_id": partner.id,
            "warehouse_id": warehouse.id,
            "order_line": lines,
        }
        so = Sale.create(so_values)
        so.action_confirm()
        return so

    @classmethod
    def _confirm_pick_ship(cls, so):
        pick = so.mapped("picking_ids").filtered(
            lambda p: p.picking_type_subcode == "PICK"
        )
        pick.action_confirm()
        pick.action_assign()
        for pack_op in pick.pack_operation_ids:
            pack_op.qty_done = pack_op.product_qty
        pick.action_done()
        ship = so.mapped("picking_ids").filtered(
            lambda p: p.picking_type_code == "outgoing"
        )
        ship.action_confirm()
        ship.action_assign()
        for pack_op in ship.pack_operation_ids:
            pack_op.qty_done = pack_op.product_qty
        ship.action_done()

    @freeze_time("2021-01-01 07:10:00")
    def test_00(self):
        self.stock_profile._compute_abc_classification()
        product_classification1 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product1.id),
            ]
        )
        product_classification2 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product2.id),
            ]
        )

        product_classification3 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product3.id),
            ]
        )

        product_classification4 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product4.id),
            ]
        )

        product_classification5 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product5.id),
            ]
        )

        product_classification6 = self.env["abc.classification.product.level"].search(
            [
                ("profile_id", "=", self.stock_profile.id),
                ("product_id", "=", self.product6.id),
            ]
        )

        self.assertEqual(product_classification1.computed_level_id.name, "A")
        self.assertEqual(product_classification3.computed_level_id.name, "A")
        self.assertEqual(product_classification5.computed_level_id.name, "A")
        self.assertEqual(product_classification2.computed_level_id.name, "B")
        self.assertEqual(product_classification6.computed_level_id.name, "B")
        self.assertEqual(product_classification4.computed_level_id.name, "C")
