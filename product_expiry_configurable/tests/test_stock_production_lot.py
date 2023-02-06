from datetime import datetime

import freezegun

from odoo import fields
from odoo.tests import SavepointCase
from odoo.tests.common import Form


class TestProductCategory(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductCategory, cls).setUpClass()

        cls.ProductCategory = cls.env["product.category"]
        cls.ProductProduct = cls.env["product.product"]
        cls.StockProductionLot = cls.env["stock.production.lot"]
        cls.ProductCategory._parent_store_compute()
        cls.categ_lvl = cls.env.ref("product.product_category_all")
        cls.categ_lvl_1 = cls.ProductCategory.create(
            {"name": "level_1", "parent_id": cls.categ_lvl.id}
        )
        cls.categ_lvl_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1", "parent_id": cls.categ_lvl_1.id}
        )

        cls.categ_lvl_1_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1_1", "parent_id": cls.categ_lvl_1_1.id}
        )
        cls.product = cls.ProductProduct.create(
            {
                "name": "test product",
                "categ_id": cls.categ_lvl_1_1_1.id,
                "tracking": "lot",
                "type": "product",
            }
        )

    def test_product_current_date(self):
        """
        Test case:
              By default compute_dates_from is "current_date".
              Product alert_time, use_time, removal_time
              and expiration_time are set to 2 each of them.
              Create product lot.
        Expected result:
             The expected values of lot alert_date, use_date, removal_date and expiration_date
              are 2 days after current_date.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time", "expiration_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date", "expiration_date"]

        for time in _get_times():
            setattr(self.product, "specific_%s" % time, 2)

        with freezegun.freeze_time("2022-02-10 10:00:00"):

            lot = self.StockProductionLot.create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "company_id": self.env.company.id,
                }
            )
            for date in _get_dates():
                self.assertEqual(
                    fields.Datetime.to_string(getattr(lot, date)), "2022-02-12 10:00:00"
                )

    def test_product_expiration_date(self):
        """
        Test case:
              Set product compute_dates_from to "expiration_date".
              Product alert_time, use_time and removal_time are set to 2 each of them.
              Create product lot with expiration_date.
        Expected result:
             The expected values of lot alert_date, use_date, removal_date and expiration_date
              are 2 days before expiration_date.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date"]

        self.product.specific_compute_dates_from = "expiration_date"

        for time in _get_times():
            setattr(self.product, "specific_%s" % time, 2)

        with freezegun.freeze_time("2022-02-12 10:00:00"):

            lot = self.StockProductionLot.create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "expiration_date": datetime(2022, 2, 28, 10, 0, 0),
                    "company_id": self.env.company.id,
                }
            )
            for date in _get_dates():
                self.assertEqual(
                    fields.Datetime.to_string(getattr(lot, date)), "2022-02-26 10:00:00"
                )

    def test_product_wo_tracking(self):
        """
        Test case:
              Create a product without tracking.
        Expected result:
             The expected values of lot alert_date, use_date, removal_date and expiration_date
              are False
        """
        product = self.ProductProduct.create(
            {
                "name": "test product",
                "categ_id": self.categ_lvl_1_1_1.id,
                "tracking": "none",
            }
        )
        lot = self.StockProductionLot.create(
            {
                "name": "lot1",
                "product_id": product.id,
                "company_id": self.env.company.id,
            }
        )

        def _get_dates():
            return ["alert_date", "use_date", "removal_date", "expiration_date"]

        for date in _get_dates():
            self.assertFalse(getattr(lot, date))

    def test_onchange_product_expiration_date(self):
        """
        Test case:
              Create a product with compute_dates_from = 'expiration_date'.
              Create lot without expiration_date.
              Set lot expiration_date after being created.

        Expected result:
             First dates are expected to be False.
             After adding the expiration_date, the fields alert_date, use_date and removal_date
             should be computed according to 'expiration_date'.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date"]

        self.product.specific_compute_dates_from = "expiration_date"

        for time in _get_times():
            setattr(self.product, "specific_%s" % time, 2)

        with freezegun.freeze_time("2022-02-12 10:00:00"):
            lot = self.StockProductionLot.create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "company_id": self.env.company.id,
                }
            )
            for date in _get_dates():
                self.assertEqual(fields.Datetime.to_string(getattr(lot, date)), False)
            self.assertFalse(lot.expiration_date)

            with Form(lot) as lot_form:
                lot_form.expiration_date = datetime(2022, 2, 28, 10, 0, 0)
                for date in _get_dates():
                    self.assertEqual(
                        fields.Datetime.to_string(getattr(lot_form, date)),
                        "2022-02-26 10:00:00",
                    )

    def test_cron_expiration_date_reached(self):
        """
        Test case:
               Create a product with compute_dates_from = 'expiration_date'
               and configure durations.
               Create lot with a past expiration_date.
               Run manually cron setting a date after expiration_date and
               the other dates.

        Expected result:
               Activities warning the different lot expiry times
               should rise.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time"]

        def _get_dates():
            return ["expiration_date", "use_date", "removal_date"]

        self.product.specific_compute_dates_from = "expiration_date"

        for time in _get_times():
            setattr(self.product, "specific_%s" % time, 2)

        lot = self.StockProductionLot.create(
            {
                "name": "lot1",
                "product_id": self.product.id,
                "company_id": self.env.company.id,
                "expiration_date": datetime(2021, 2, 28, 10, 0, 0),
            }
        )

        stock_location = self.env["stock.location"].create(
            {"name": "Internal test location", "usage": "internal"}
        )

        self.env["stock.quant"].create(
            {
                "location_id": stock_location.id,
                "lot_id": lot.id,
                "quantity": 10,
                "product_id": self.product.id,
                "company_id": self.env.company.id,
            }
        )

        with freezegun.freeze_time("2022-02-12 10:00:00"):
            counter = 1
            for date in _get_dates():
                self.assertFalse(getattr(lot, "%s_reminded" % date))
                self.env["stock.production.lot"]._expiry_date_exceeded(date_field=date)
                activity_id = self.env.ref(
                    "product_expiry_configurable.mail_activity_type_expiry_date_reached"
                ).id
                activity_count = self.env["mail.activity"].search_count(
                    [
                        ("activity_type_id", "=", activity_id),
                        (
                            "res_model_id",
                            "=",
                            self.env.ref("stock.model_stock_production_lot").id,
                        ),
                        ("res_id", "=", lot.id),
                    ]
                )
                self.assertTrue(getattr(lot, "%s_reminded" % date))
                self.assertEqual(activity_count, counter)
                counter += 1
