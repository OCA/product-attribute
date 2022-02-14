# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests import Form, common


@freeze_time("2021-04-01 00:00:00")
class TestSaleProductClassificationCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Mr. Odoo"})
        cls.profile = cls.env["abc.classification.profile"].create(
            {
                "name": "Test Profile",
                "classification_type": "fixed",
                "data_source": "sale_report",
                "value_criteria": "sold_delivered_value",
            }
        )
        cls.a = cls.env["abc.classification.profile.level"].create(
            {"profile_id": cls.profile.id, "fixed": 10000}
        )
        cls.b = cls.env["abc.classification.profile.level"].create(
            {"profile_id": cls.profile.id, "fixed": 5000}
        )
        cls.c = cls.env["abc.classification.profile.level"].create(
            {"profile_id": cls.profile.id, "fixed": 2500}
        )
        cls.d = cls.env["abc.classification.profile.level"].create(
            {"profile_id": cls.profile.id, "fixed": 0}
        )
        # Quickly generate 5 products with a different price each
        cls.products = cls.env["product.product"].create(
            [
                {
                    "name": "Test product {}".format(i + 1),
                    "type": "service",
                    "list_price": i + 1,
                }
                for i in range(5)
            ]
        )
        (cls.prod_1, cls.prod_2, cls.prod_3, cls.prod_4, cls.prod_5) = cls.products
        cls.products.write(
            {
                "create_date": "2021-03-01",
                "abc_classification_profile_id": cls.profile.id,
            }
        )
        # Let's prepare some sales for them. This will be the final calendar:
        # +-------------+-------+------+------+------+------+
        # |    date     |  p1   |  p2  |  p3  |  p4  |  p5  |
        # +-------------+-------+------+------+------+------+
        # | 2021-01-01  |  1000 | 2000 |      |      | 5000 |
        # | 2021-02-01  |  1000 |      | 3000 | 4000 |      |
        # | 2021-03-01  |  1000 |      |      | 4000 |      |
        # | 2021-04-01  |  1000 |      | 3000 |      |      |
        # | TOTALS:     |  4000 | 2000 | 6000 | 8000 | 5000 |
        # +-------------+-------+------+------+------+------+
        cls.sales_calendar = {
            "2021-01-01": cls.prod_1 | cls.prod_2 | cls.prod_5,
            "2021-02-01": cls.prod_1 | cls.prod_3 | cls.prod_4,
            "2021-03-01": cls.prod_1 | cls.prod_4,
            "2021-04-01": cls.prod_1 | cls.prod_3,
        }
        for date, products in cls.sales_calendar.items():
            cls._create_sale(date, cls.partner, products)

    @classmethod
    def _create_sale(cls, date, partner, products, qty=1000):
        """Simple sale creation"""
        sale_form = Form(cls.env["sale.order"])
        sale_form.partner_id = partner
        for product in products:
            with sale_form.order_line.new() as line_form:
                line_form.product_id = product
                line_form.product_uom_qty = qty
                line_form.qty_delivered = qty
        sale_order = sale_form.save()
        sale_order.action_confirm()
        # Force the date so to reproduce the calendar
        sale_order.date_order = date

    def _test_product_classification(self, classifications):
        """Helper to assert classifications in batch. It's expected to come
        as dict of key product record and value string classification"""
        for product, classification in classifications.items():
            self.assertEqual(product.abc_classification_level_id, classification)
