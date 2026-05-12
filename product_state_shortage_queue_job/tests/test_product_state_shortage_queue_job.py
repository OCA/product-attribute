# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.queue_job.tests.common import JobMixin


class TestProductStateShortageQueueJob(TransactionCase, JobMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_state_cron = cls.env.ref(
            "product_state_shortage.ir_cron_reset_product_shortage_state"
        )
        cls.reset_state_cron.run_as_queue_job = True

        cls.shortage_state_1 = cls.env["product.state"].create(
            {
                "name": "Shortage 1",
                "code": "S1",
                "is_shortage": True,
            }
        )
        cls.shortage_state_2 = cls.env["product.state"].create(
            {
                "name": "Shortage 2",
                "code": "S2",
                "is_shortage": True,
            }
        )
        cls.default_state = cls.env["product.template"]._get_default_product_state()
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "product_state_id": cls.shortage_state_1.id,
                "detailed_type": "product",
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "product_state_id": cls.shortage_state_2.id,
                "detailed_type": "product",
            }
        )
        cls.wh = cls.env["stock.warehouse"].search([], limit=1)
        cls.loc_shelf_1 = cls.env["stock.location"].create(
            {"name": "Shelf 1", "location_id": cls.wh.lot_stock_id.id}
        )

    def test_log_after_reset_state_cron(self):
        counter = self.job_counter()

        self.reset_state_cron.method_direct_trigger()

        new_jobs = counter.search_created()
        self.assertEqual(len(new_jobs), 1)

        new_jobs.write({"state": "started"})

        (
            self.product_1 | self.product_2
        ).product_tmpl_id._before_reset_default_state_hook()

        messages = new_jobs.mapped("message_ids.body")
        self.assertTrue(any(self.product_1.name in msg for msg in messages))
        self.assertTrue(any(self.product_2.name in msg for msg in messages))
