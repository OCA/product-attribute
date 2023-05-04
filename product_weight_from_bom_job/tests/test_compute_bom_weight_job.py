# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBomWeightCompute(TransactionCase):
    def test_cron_weight_update_job(self):
        self.env["product.product"].cron_recompute_bom_weight()
        product_job = self.env["queue.job"].search(
            [("name", "=", "product.product.update_weight_from_bom")]
        )
        self.assertTrue(product_job)
