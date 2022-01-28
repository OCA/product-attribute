# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests.common import SavepointCase


class TestABCClassificationProfile(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestABCClassificationProfile, cls).setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {"name": "Unittest partner", "ref": "12344566777878"}
        )

        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.warehouse.write(
            {
                "name": "Test Warehouse",
                "reception_steps": "one_step",
                "delivery_steps": "ship_only",
                "code": "TST",
            }
        )

        cls.stock_profile = cls.env.ref(
            "product_abc_classification_sale_stock."
            "abc_classification_profile_sale_stock"
        )
        cls.level_A = cls.env.ref(
            "product_abc_classification_sale_stock.abc_classification_level_a"
        )
        cls.level_B = cls.env.ref(
            "product_abc_classification_sale_stock.abc_classification_level_b"
        )
        cls.level_C = cls.env.ref(
            "product_abc_classification_sale_stock.abc_classification_level_c"
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
        # Special case where the product is not yet sold nor delivered
        cls.product_new = cls.env["product.product"].create(
            {
                "name": "product_new",
                "uom_id": cls.env.ref("product.product_uom_unit").id,
                "type": "product",
                "default_code": "345789733",
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
            qty={
                cls.product1.name: 80,
                cls.product2.name: 10,
                cls.product3.name: 30,
            },
        )
        cls._confirm_ship(cls.so1)

        cls.so2 = cls._confirm_sale_order(
            products=[cls.product4, cls.product5, cls.product6],
            qty={
                cls.product4.name: 5,
                cls.product5.name: 30,
                cls.product6.name: 25,
            },
        )
        cls._confirm_ship(cls.so2)

        cls.so3 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 75}
        )
        cls._confirm_ship(cls.so3)

        cls.so3 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 75}
        )
        cls._confirm_ship(cls.so3)

        cls.so4 = cls._confirm_sale_order(
            products=[cls.product1], qty={cls.product1.name: 25}
        )
        cls._confirm_ship(cls.so4)

        cls.so5 = cls._confirm_sale_order(
            products=[cls.product3, cls.product5],
            qty={cls.product3.name: 90, cls.product5.name: 50},
        )
        cls._confirm_ship(cls.so5)

        cls.so6 = cls._confirm_sale_order(
            products=[cls.product6], qty={cls.product6.name: 30}
        )
        cls._confirm_ship(cls.so6)

    @classmethod
    def _create_availability(cls, product):
        update_qty_wizard = cls.env["stock.change.product.qty"].create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "new_quantity": 500,
                "location_id": cls.warehouse.lot_stock_id.id,
            }
        )
        update_qty_wizard.change_product_qty()

    @classmethod
    def _confirm_sale_order(cls, products, qty, partner=None):
        if partner is None:
            partner = cls.partner
        warehouse = cls.warehouse
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
    def _confirm_ship(cls, so):
        pick = so.mapped("picking_ids")
        pick.action_confirm()
        pick.action_assign()
        for pack_op in pick.pack_operation_ids:
            pack_op.qty_done = pack_op.product_qty
        pick.action_done()

    def _assertLevelIs(self, product, level_name):
        levels = product.abc_classification_product_level_ids
        self.assertEqual(
            levels.computed_level_id.name,
            level_name,
            "{} should be classified as {}".format(product.name, level_name),
        )
        levels = product.product_tmpl_id.abc_classification_product_level_ids
        self.assertEqual(
            levels.computed_level_id.name,
            level_name,
            "{} template should be classified as {}".format(product.name, level_name),
        )

    @freeze_time("2021-01-01 07:10:00")
    def test_00(self):
        # test computed classification and check that the classification is
        # also set on the product_templale
        self.stock_profile._compute_abc_classification()
        self._assertLevelIs(self.product1, "a")
        self._assertLevelIs(self.product3, "a")
        self._assertLevelIs(self.product5, "b")
        self._assertLevelIs(self.product6, "b")
        self._assertLevelIs(self.product2, "c")
        self._assertLevelIs(self.product4, "c")
        self._assertLevelIs(self.product_new, "c")

    @freeze_time("2021-01-01 07:10:00")
    def test_01(self):
        # test computed classification and check that inactive products are
        # not taken into account
        self.product1.active = False
        self.product1.refresh()
        self.stock_profile._compute_abc_classification()
        self.assertFalse(self.product1.abc_classification_product_level_ids)
        self.product1.active = True
        self.product1.refresh()
        self.stock_profile._compute_abc_classification()
        self.assertTrue(self.product1.abc_classification_product_level_ids)
        self.product1.active = False
        self.product1.refresh()
        self.stock_profile._compute_abc_classification()
        self.assertFalse(self.product1.abc_classification_product_level_ids)

    @freeze_time("2021-01-01 07:10:00")
    def test_02(self):
        # check that a line is created into the history value for each
        # computed classification level each time a compute is done
        levels = self.product1.abc_classification_product_level_ids
        self.assertFalse(levels.sale_stock_level_history_ids)
        self.stock_profile._compute_abc_classification()
        levels = self.product1.abc_classification_product_level_ids
        self.assertEqual(len(levels.sale_stock_level_history_ids), 1)
        self.stock_profile._compute_abc_classification()
        self.assertEqual(len(levels.sale_stock_level_history_ids), 2)

