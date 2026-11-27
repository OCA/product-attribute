# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductStateSale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.state_sellable = cls.env.ref("product_state.product_state_sellable")
        cls.state_blocked = cls.env["product.state"].create(
            {"name": "Not Sellable", "code": "not_sellable", "can_be_sold": False}
        )
        cls.product_ok = cls.env["product.product"].create(
            {"name": "Sellable Product", "product_state_id": cls.state_sellable.id}
        )
        cls.product_blocked = cls.env["product.product"].create(
            {"name": "Blocked Product", "product_state_id": cls.state_blocked.id}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Customer"})

    def _create_order(self, product):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create({"product_id": product.id, "product_uom_qty": 1})
                ],
            }
        )

    def test_domain_excludes_blocked_products(self):
        domain = self.env["sale.order.line"]._domain_product_id()
        products = self.env["product.product"].search(domain)
        self.assertIn(self.product_ok, products)
        self.assertNotIn(self.product_blocked, products)

    def test_sellable_product_allowed(self):
        order = self._create_order(self.product_ok)
        self.assertEqual(order.order_line.product_id, self.product_ok)

    def test_blocked_product_refused(self):
        with self.assertRaisesRegex(ValidationError, "cannot be sold"):
            self._create_order(self.product_blocked)

    def test_blocked_product_refused_on_write(self):
        order = self._create_order(self.product_ok)
        with self.assertRaisesRegex(ValidationError, "cannot be sold"):
            order.order_line.product_id = self.product_blocked

    def test_existing_line_not_affected_by_later_state_change(self):
        order = self._create_order(self.product_ok)
        self.product_ok.product_state_id = self.state_blocked
        # Changing unrelated fields on the line must still be possible
        order.order_line.product_uom_qty = 2
        self.assertEqual(order.order_line.product_uom_qty, 2)

    def test_state_flag_on_products(self):
        template = self.product_ok.product_tmpl_id
        self.assertTrue(template.product_state_can_be_sold)
        self.assertTrue(self.product_ok.product_state_can_be_sold)
        self.assertFalse(self.product_blocked.product_state_can_be_sold)
        self.assertIn(
            self.product_blocked.product_tmpl_id,
            self.env["product.template"].search(
                [("product_state_can_be_sold", "=", False)]
            ),
        )
        self.state_blocked.can_be_sold = True
        self.assertTrue(self.product_blocked.product_state_can_be_sold)
