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
            }
        )

    def test_product_current_date(self):
        """
            Test case:
                  By default compute_dates_from is "current_date".
                  Product alert_time, use_time, removal_time
                  and life_time are set to 2 each of them.
                  Create product lot.
            Expected result:
                 The expected values of lot alert_date, use_date, removal_date and life_date
                  are 2 days after current_date.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time", "life_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date", "life_date"]

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

    def test_product_life_date(self):
        """
            Test case:
                  Set product compute_dates_from to "life_date".
                  Product alert_time, use_time and removal_time are set to 2 each of them.
                  Create product lot with life_date.
            Expected result:
                 The expected values of lot alert_date, use_date, removal_date and life_date
                  are 2 days before life_date.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date"]

        self.product.specific_compute_dates_from = "life_date"

        for time in _get_times():
            setattr(self.product, "specific_%s" % time, 2)

        with freezegun.freeze_time("2022-02-12 10:00:00"):

            lot = self.StockProductionLot.create(
                {
                    "name": "lot1",
                    "product_id": self.product.id,
                    "life_date": datetime(2022, 2, 28, 10, 0, 0),
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
                  The expected values of lot alert_date, use_date, removal_date and life_date
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
            return ["alert_date", "use_date", "removal_date", "life_date"]

        for date in _get_dates():
            self.assertFalse(getattr(lot, date))

    def test_onchange_product_life_date(self):
        """
       Test case:
             Create a product with compute_dates_from = 'life_date'.
             Create lot without life_date.
             Set lot life_date after being created.

       Expected result:
            First dates are expected to be computed by the standard odoo method.
            After adding the life_date, the alert_date, use_date and removal_date
            should be computed according to 'life_date'.
        """

        def _get_times():
            return ["alert_time", "use_time", "removal_time"]

        def _get_dates():
            return ["alert_date", "use_date", "removal_date"]

        self.product.specific_compute_dates_from = "life_date"

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
                self.assertEqual(
                    fields.Datetime.to_string(getattr(lot, date)), "2022-02-14 10:00:00"
                )
            self.assertFalse(lot.life_date)

            with Form(lot) as lot_form:
                lot_form.life_date = datetime(2022, 2, 28, 10, 0, 0)
                for date in _get_dates():
                    self.assertEqual(
                        fields.Datetime.to_string(getattr(lot_form, date)),
                        "2022-02-26 10:00:00",
                    )
