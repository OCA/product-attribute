# Copyright 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestStockLotExpirationDates(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_model = cls.env["product.product"]
        cls.production_lot_model = cls.env["stock.lot"]
        cls.category = cls.env.ref("product.product_category_all")
        cls.category_2 = cls.env.ref("product.product_category_2")
        cls.category_3 = cls.env.ref("product.product_category_3")
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.product = cls.product_model.create(
            {
                "name": "Unittest product",
                "type": "product",
                "categ_id": cls.category.id,
                "use_time": 10,
                "expiration_time": 11,
                "alert_time": 12,
                "removal_time": 13,
            }
        )
        cls.production_lot = cls.production_lot_model.create(
            {
                "name": "000001",
                "product_id": cls.product.id,
                "company_id": cls.env.company.id,
            }
        )

        cls.product_2 = cls.product_model.create(
            {
                "name": "Unittest product 2",
                "type": "product",
                "categ_id": cls.category_2.id,
                "use_time": -13,
                "expiration_time": -12,
                "alert_time": -11,
                "removal_time": -10,
            }
        )
        cls.production_lot_2 = cls.production_lot_model.create(
            {
                "name": "000001",
                "product_id": cls.product_2.id,
                "company_id": cls.env.company.id,
            }
        )

        cls.product_3 = cls.product_model.create(
            {
                "name": "Unittest product 3",
                "type": "product",
                "categ_id": cls.category_3.id,
                "use_time": 0,
                "expiration_time": 0,
                "alert_time": 0,
                "removal_time": 0,
            }
        )
        cls.production_lot_3 = cls.production_lot_model.create(
            {
                "name": "000001",
                "product_id": cls.product_3.id,
                "company_id": cls.env.company.id,
            }
        )

        day_1 = timedelta(days=1)
        cls.date_20 = datetime.strptime("2016-12-20 10:00:00", "%Y-%m-%d %H:%M:%S")
        cls.date_21 = cls.date_20 + day_1
        cls.date_22 = cls.date_21 + day_1
        cls.date_23 = cls.date_22 + day_1
        cls.date_24 = cls.date_23 + day_1
        cls.date_25 = cls.date_24 + day_1
        cls.date_26 = cls.date_25 + day_1

    def _set_lot_base_date(self, base_date):
        """It is faster to set directly the param instead
        of relying on the config setting execution"""
        self.env["ir.config_parameter"].set_param(
            "stock_production_lot_expired_date.production_lot_base_date", base_date
        )

    def test_1_onchange_use_date(self):
        for base_date in [None, "alert", "expiration", "removal", "use"]:
            self._set_lot_base_date(base_date)
            for production_lot in [
                self.production_lot,
                self.production_lot_2,
                self.production_lot_3,
            ]:
                production_lot.use_date = False
                production_lot.expiration_date = False
                production_lot.alert_date = False
                production_lot.removal_date = False
                production_lot.use_date = self.date_23
                production_lot.onchange_use_date()
                date_must_change = (
                    base_date == "use" and production_lot != self.production_lot_3
                )
                self.assertEqual(production_lot.use_date, self.date_23)
                self.assertEqual(
                    production_lot.expiration_date,
                    self.date_24 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.alert_date,
                    self.date_25 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.removal_date,
                    self.date_26 if date_must_change else False,
                )
                # Check the onchange does not fails with no value
                production_lot.use_date = False
                production_lot.onchange_use_date()

    def test_2_onchange_expiration_date(self):
        for base_date in [None, "alert", "expiration", "removal", "use"]:
            self._set_lot_base_date(base_date)
            for production_lot in [
                self.production_lot,
                self.production_lot_2,
                self.production_lot_3,
            ]:
                production_lot.use_date = False
                production_lot.expiration_date = False
                production_lot.alert_date = False
                production_lot.removal_date = False
                production_lot.expiration_date = self.date_23
                production_lot.onchange_expiration_date()
                date_must_change = (
                    base_date == "expiration"
                    and production_lot != self.production_lot_3
                )
                self.assertEqual(
                    production_lot.use_date,
                    self.date_22 if date_must_change else False,
                )
                self.assertEqual(production_lot.expiration_date, self.date_23)
                self.assertEqual(
                    production_lot.alert_date,
                    self.date_24 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.removal_date,
                    self.date_25 if date_must_change else False,
                )
                # Check the onchange not fails with no value
                production_lot.expiration_date = False
                production_lot.onchange_expiration_date()

    def test_3_onchange_alert_date(self):
        for base_date in [None, "alert", "expiration", "removal", "use"]:
            self._set_lot_base_date(base_date)
            for production_lot in [
                self.production_lot,
                self.production_lot_2,
                self.production_lot_3,
            ]:
                production_lot.use_date = False
                production_lot.expiration_date = False
                production_lot.alert_date = False
                production_lot.removal_date = False
                production_lot.alert_date = self.date_23
                production_lot.onchange_alert_date()
                date_must_change = (
                    base_date == "alert" and production_lot != self.production_lot_3
                )
                self.assertEqual(
                    production_lot.use_date,
                    self.date_21 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.expiration_date,
                    self.date_22 if date_must_change else False,
                )
                self.assertEqual(production_lot.alert_date, self.date_23)
                self.assertEqual(
                    production_lot.removal_date,
                    self.date_24 if date_must_change else False,
                )
                # Check the onchange not fails with no value
                production_lot.alert_date = False
                production_lot.onchange_alert_date()

    def test_4_onchange_removal_date(self):
        for base_date in [None, "alert", "expiration", "removal", "use"]:
            self._set_lot_base_date(base_date)
            for production_lot in [
                self.production_lot,
                self.production_lot_2,
                self.production_lot_3,
            ]:
                production_lot.use_date = False
                production_lot.expiration_date = False
                production_lot.alert_date = False
                production_lot.removal_date = False
                production_lot.removal_date = self.date_23
                production_lot.onchange_removal_date()
                date_must_change = (
                    base_date == "removal" and production_lot != self.production_lot_3
                )
                self.assertEqual(
                    production_lot.use_date,
                    self.date_20 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.expiration_date,
                    self.date_21 if date_must_change else False,
                )
                self.assertEqual(
                    production_lot.alert_date,
                    self.date_22 if date_must_change else False,
                )
                self.assertEqual(production_lot.removal_date, self.date_23)
                # Check the onchange not fails with no value
                production_lot.removal_date = False
                production_lot.onchange_removal_date()
