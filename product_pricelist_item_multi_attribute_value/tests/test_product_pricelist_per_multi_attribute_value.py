# Copyright 2025 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import CommonPricelistPerMultiAttributeValue


class TestPricelistMultiAttributeValue(CommonPricelistPerMultiAttributeValue):
    def test_product_alu_black(self):
        sol = self.new_sale_line(self.product_alu_black)
        self.assertEqual(sol.price_unit, 175)

    def test_product_steel_white(self):
        sol = self.new_sale_line(self.product_steel_white)
        self.assertEqual(sol.price_unit, 150)

    def test_product_alu_white(self):
        sol = self.new_sale_line(self.product_alu_white)
        self.assertEqual(sol.price_unit, 175)

    def test_product_steel_white_no_additional_price(self):
        self.color_price.unlink()
        sol = self.new_sale_line(self.product_steel_white)
        self.assertEqual(sol.price_unit, 100)

    def test_product_steel_white_action_update_prices(self):
        sol = self.new_sale_line(self.product_steel_white)
        self.color_price.write({"additional_price": 1000})
        self.sale.action_update_prices()
        self.assertEqual(sol.price_unit, 1100)
