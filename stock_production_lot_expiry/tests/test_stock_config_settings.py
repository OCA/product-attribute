# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestStockConfigSettings(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockConfigSettings, cls).setUpClass()
        cls.StockConfigSettings = cls.env["stock.config.settings"]
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
        default_value = (
            self.StockConfigSettings.get_production_lot_expiry_date_field()
        )
        xml_data_value = self.env.ref(
            "stock_production_lot_expiry."
            "default_stock_production_lot_expiry_field_name"
        ).value
        self.assertEqual(default_value, "removal_date")
        self.assertEqual(xml_data_value, default_value)
        self.StockConfigSettings.create(
            {"production_lot_expiry_date_field": "life_date"}
        ).execute()
        default_value = (
            self.StockConfigSettings.get_production_lot_expiry_date_field()
        )
        self.assertEqual("life_date", default_value)
