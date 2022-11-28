# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResConfigSettings(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestResConfigSettings, cls).setUpClass()
        cls.ResConfigSettings = cls.env["res.config.settings"]
        cls.IrConfigParameter = cls.env["ir.config_parameter"]

    def test_00(self):
        """
        Data:
            nihil
        Test case:
            Update and load config
        Expected result:
            Values retrieved are those saved
        """
        default_value = self.ResConfigSettings.get_production_lot_expiry_date_field()
        xml_data_value = self.env.ref(
            "stock_production_lot_expiry."
            "default_stock_production_lot_expiry_field_name"
        ).value
        self.assertEqual(default_value, "removal_date")
        self.assertEqual(xml_data_value, default_value)
        self.ResConfigSettings.create(
            {"production_lot_expiry_date_field": "expiration_date"}
        ).execute()
        default_value = self.ResConfigSettings.get_production_lot_expiry_date_field()
        self.assertEqual("expiration_date", default_value)
