# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .common import Common


class TestProductPackagingContainerDepositMixin(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import (
            ContainerDepositOrderLineTest,
            ContainerDepositOrderTest,
        )

        cls.loader.update_registry(
            (
                ContainerDepositOrderTest,
                ContainerDepositOrderLineTest,
            )
        )

    def setUp(self):
        super().setUp()
        self.order = self.env["container.deposit.order.test"].create(
            {
                "company_id": self.env.company.id,
                "partner_id": self.env.ref("base.res_partner_12").id,
            }
        )

    def test_implemented_get_order_line_field(self):
        self.assertEqual(
            self.env["container.deposit.order.test"]._get_order_line_field(),
            "order_line",
        )

    def test_implemented_get_product_qty_field(self):
        self.assertEqual(
            self.env["container.deposit.order.line.test"]._get_product_qty_field(),
            "product_qty",
        )

    def test_get_order_lines_container_deposit_quantities(self):
        deposit_product_qties = (
            self.order.order_line._get_order_lines_container_deposit_quantities()
        )
        self.assertEqual(deposit_product_qties, {})
        self.env["container.deposit.order.line.test"].create(
            {
                "order_id": self.order.id,
                "name": self.product_a.name,
                "product_id": self.product_a.id,
                "product_qty": 50,
            }
        )
        deposit_product_qties = (
            self.order.order_line._get_order_lines_container_deposit_quantities()
        )
        self.assertEqual(deposit_product_qties, {self.box: [2.0, 0]})

    def test_implemented_get_product_qty_delivered_received_field(self):
        self.assertEqual(
            self.env[
                "container.deposit.order.line.test"
            ]._get_product_qty_delivered_received_field(),
            "qty_delivered",
        )

    def test_product_container_deposit_order(self):
        self.env["container.deposit.order.line.test"].create(
            {
                "order_id": self.order.id,
                "name": self.product_a.name,
                "product_id": self.product_a.id,
                "product_qty": 50,
            }
        )
        deposit_lines = self.order.order_line.filtered(
            lambda ol: ol.product_id
            in self.product_a.mapped(
                "packaging_ids.package_type_id.container_deposit_product_id"
            )
        )
        self.assertEqual(len(deposit_lines), 1)

    def test_order_product_packaging_container_deposit_quantities_case1(self):
        """
        Case 1: Product A | qty = 280. Result:
                280 // 240 = 1 => add order line for 1 Pallet
                280 // 24 (biggest PACK) => add order line for 11 boxes of 24
        """
        self.env["container.deposit.order.line.test"].create(
            [
                {
                    "order_id": self.order.id,
                    "name": self.product_a.name,
                    "product_id": self.product_a.id,
                    "product_qty": 280,
                },
                {
                    "order_id": self.order.id,
                    "name": self.product_c.name,
                    "product_id": self.product_c.id,
                    "product_qty": 1,
                },
            ]
        )

        pallet_line = self.order.order_line.filtered(
            lambda ol: ol.product_id == self.pallet
        )
        box_line = self.order.order_line.filtered(lambda ol: ol.product_id == self.box)
        self.assertEqual(pallet_line.product_qty, 1)
        self.assertEqual(box_line.product_qty, 11)

    def test_order_product_packaging_container_deposit_quantities_case2(self):
        """
        Case 2: Product A | qty = 280 and packaging=Box of 12. Result:
            280 // 240 = 1 => add order line for 1 Pallet
            280 // 12 (forced packaging for Boxes) => add order line for 23 boxes of 12
        """
        self.env["container.deposit.order.line.test"].create(
            {
                "order_id": self.order.id,
                "name": self.product_a.name,
                "product_id": self.product_a.id,
                "product_qty": 280,
                # Box of 12
                "product_packaging_id": self.packaging[0].id,
            },
        )
        # Filter lines with boxes
        box_lines = self.order.order_line.filtered(lambda ol: ol.product_id == self.box)
        self.assertEqual(box_lines[0].product_qty, 23)

    def test_order_product_packaging_container_deposit_quantities_case3(self):
        """
        Case 3: Product A & Product B. Both have a deposit of 1 box of 24. Result:
                Only one line for 2 boxes of 24
        """
        self.env["container.deposit.order.line.test"].create(
            [
                {
                    "order_id": self.order.id,
                    "name": self.product_a.name,
                    "product_id": self.product_a.id,
                    "product_qty": 24,
                },
                {
                    "order_id": self.order.id,
                    "name": self.product_b.name,
                    "product_id": self.product_b.id,
                    "product_qty": 24,
                },
            ]
        )
        box_lines = self.order.order_line.filtered(lambda ol: ol.product_id == self.box)
        self.assertEqual(box_lines[0].product_qty, 2)

    def test_order_product_packaging_container_deposit_quantities_case4(self):
        """
        Case 4: Product A | qty = 24. Result:
                24 // 24 (biggest PACK) => add order line for 1 box of 24
                Product A | Increase to 48. Result:
                48 // 24 (biggest PACK) =>  recompute previous order line with 2 boxes of 24
                Add manually Product A container deposit (Box). Result:
                1 order line with 2 boxes of 24 (System added)
                + 1 order line with 1 box (manually added)
        """
        order_line = self.env["container.deposit.order.line.test"].create(
            {
                "order_id": self.order.id,
                "name": self.product_a.name,
                "product_id": self.product_a.id,
                "product_qty": 24,
            },
        )
        order_line.write({"product_qty": 48})
        deposit_line = self.order.order_line.filtered(
            lambda ol: ol.product_id
            in self.product_a.mapped(
                "packaging_ids.package_type_id.container_deposit_product_id"
            )
        )
        self.assertEqual(deposit_line.name, "Box")
        self.assertEqual(deposit_line.product_qty, 2.0)

        # Add manually 1 box
        self.env["container.deposit.order.line.test"].create(
            {
                "order_id": self.order.id,
                "name": self.package_type_box.container_deposit_product_id.name,
                "product_id": self.package_type_box.container_deposit_product_id.id,
                "product_qty": 1,
            }
        )

        box_lines = self.order.order_line.filtered(lambda ol: ol.product_id == self.box)
        self.assertEqual(box_lines[0].product_qty, 2)
        self.assertEqual(box_lines[1].product_qty, 1)

    def test_order_product_packaging_container_deposit_quantities_case5(self):
        """
        Case 7.1: Product A | qty = 280
                Product A | Partial shipment (qty_delivered = 140). Result:
                Received 140 // 280 = 0 Pallet
                Received 140 // 24 = 5 Boxes
        Case 7.2: Product A | Increase delivered quantity (qty_delivered = 200). Result:

                Received 200 // 280 = 0 Pallet
                Received 200 // 24 = 5 Boxes
        """
        self.env["container.deposit.order.line.test"].create(
            [
                {
                    "order_id": self.order.id,
                    "name": self.product_a.name,
                    "product_id": self.product_a.id,
                    "product_qty": 280,
                },
            ]
        )
        self.order.order_line[0].qty_delivered = 140

        pallet_line = self.order.order_line.filtered(
            lambda ol: ol.product_id == self.pallet
        )
        box_line = self.order.order_line.filtered(lambda ol: ol.product_id == self.box)
        self.assertEqual(pallet_line.qty_delivered, 0)
        self.assertEqual(box_line.qty_delivered, 5)

        self.order.order_line[0].qty_delivered = 200
        self.assertEqual(pallet_line.qty_delivered, 0)
        self.assertEqual(box_line.qty_delivered, 8)
