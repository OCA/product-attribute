# Copyright 2024 Akretion (http://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import Command as cmd
from odoo.tests.common import TransactionCase


class Test(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "test"})
        self.product = self.env["product.product"].create({"name": "test"})
        self.purchase = create_purchase(self, relative_days=10)

    def test_next_reception_date(self):
        self.purchase.button_confirm()
        self.assertEqual(
            self.purchase.date_planned.date(),
            self.product.next_reception_date,
        )

    def test_2_next_reception_date(self):
        self.purchase.button_confirm()
        self.purchase2 = create_purchase(self, relative_days=4)
        self.purchase2.button_confirm()
        # The next reception date should be updated to the earliest one
        self.assertEqual(
            self.purchase2.date_planned.date(),
            self.product.next_reception_date,
        )


def create_purchase(self, relative_days):
    return self.env["purchase.order"].create(
        {
            "partner_id": self.partner.id,
            "date_order": datetime.today() + relativedelta(days=relative_days),
            "order_line": [
                cmd.create(
                    {
                        "product_id": self.product.id,
                        "product_qty": 5,
                    }
                ),
            ],
        }
    )
