# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestProductStateAccount(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.state_sellable = cls.env.ref("product_state.product_state_sellable")
        cls.state_blocked = (
            cls.env["product.state"]
            .sudo()
            .create(
                {
                    "name": "Not Invoiceable",
                    "code": "not_invoiceable",
                    "can_be_invoiced": False,
                }
            )
        )
        cls.product_ok = cls.env["product.product"].create(
            {"name": "Invoiceable Product", "list_price": 10.0}
        )
        cls._set_state(cls.product_ok, cls.state_sellable)
        cls.product_blocked = cls.env["product.product"].create(
            {"name": "Blocked Product", "list_price": 10.0}
        )
        cls._set_state(cls.product_blocked, cls.state_blocked)

    @classmethod
    def _set_state(cls, product, state):
        """Set the product state on the template and the variant.

        With product_status installed a state given on create is discarded and
        variants carry their own state; writing the state code afterwards is
        the entry point shared by both modules. Without it the variant write
        is delegated to the template.
        """
        product.product_tmpl_id.state = state.code
        product.state = state.code

    def _create_move(self, move_type, product):
        return self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner_a.id,
                "invoice_line_ids": [
                    Command.create(
                        {"product_id": product.id, "quantity": 1, "price_unit": 10.0}
                    )
                ],
            }
        )

    def test_invoiceable_product_allowed(self):
        move = self._create_move("out_invoice", self.product_ok)
        self.assertEqual(move.invoice_line_ids.product_id, self.product_ok)

    def test_blocked_product_refused_on_customer_invoice(self):
        for move_type in ("out_invoice", "out_refund", "out_receipt"):
            with self.subTest(move_type=move_type):
                with self.assertRaisesRegex(ValidationError, "cannot be invoiced"):
                    self._create_move(move_type, self.product_blocked)

    def test_blocked_product_refused_on_write(self):
        move = self._create_move("out_invoice", self.product_ok)
        with self.assertRaisesRegex(ValidationError, "cannot be invoiced"):
            move.invoice_line_ids.product_id = self.product_blocked

    def test_blocked_product_allowed_on_vendor_bill(self):
        move = self._create_move("in_invoice", self.product_blocked)
        self.assertEqual(move.invoice_line_ids.product_id, self.product_blocked)

    def test_existing_line_not_affected_by_later_state_change(self):
        move = self._create_move("out_invoice", self.product_ok)
        self._set_state(self.product_ok, self.state_blocked)
        move.invoice_line_ids.quantity = 2
        self.assertEqual(move.invoice_line_ids.quantity, 2)
        move.action_post()
        self.assertEqual(move.state, "posted")

    def test_state_flag_on_products(self):
        template = self.product_ok.product_tmpl_id
        self.assertTrue(template.product_state_can_be_invoiced)
        self.assertTrue(self.product_ok.product_state_can_be_invoiced)
        self.assertFalse(self.product_blocked.product_state_can_be_invoiced)
        self.assertIn(
            self.product_blocked.product_tmpl_id,
            self.env["product.template"].search(
                [("product_state_can_be_invoiced", "=", False)]
            ),
        )
        self.state_blocked.sudo().can_be_invoiced = True
        self.assertTrue(self.product_blocked.product_state_can_be_invoiced)
