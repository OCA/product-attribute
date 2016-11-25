# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from datetime import datetime, date
from openerp.exceptions import ValidationError


class TestProductKosher(common.TransactionCase):

    def setUp(self):
        super(TestProductKosher, self).setUp()
        # Objects
        self.obj_product_template = self.env["product.template"]

        # Data Product
        self.product_1 = self.env.ref("product.product_product_1")
        self.product_2 = self.env.ref("product.product_product_2")
        self.product_3 = self.env.ref("product.product_product_3")

    def test_constrains_date(self):
        # CONDITION
        # date_end < date_start

        # UPDATE PRODUCT
        criteria = [
            ("id", "=", self.product_1.id)
        ]
        product = self.obj_product_template.search(
            criteria)[0]

        vals = {
            'kosher_ids': [
                (0, 0, {
                    'name': 'Certificate No.1',
                    'date_start': '2016-01-30',
                    'date_end': '2016-01-01'})
            ]
        }

        # Check Constrains
        with self.assertRaises(ValidationError):
            product.write(vals)

    def test_product_kosher_status_1(self):
        # CONDITION
        # date_start = True
        # date_end = False

        # UPDATE PRODUCT
        criteria = [
            ("id", "=", self.product_1.id)
        ]
        product = self.obj_product_template.search(
            criteria)[0]

        vals = {
            'kosher_ids': [
                (0, 0, {
                    'name': 'Certificate No.1',
                    'date_start': '2016-01-01'})
            ]
        }
        product.write(vals)
        self.assertEqual(product.kosher_state, "certified")

    def test_product_kosher_status_2(self):
        # CONDITION
        # date_start = True
        # date_end < date.now

        # UPDATE PRODUCT
        criteria = [
            ("id", "=", self.product_2.id)
        ]
        product = self.obj_product_template.search(
            criteria)[0]

        date_now = datetime.now().strftime("%Y-%m-%d")

        date_end = date.fromordinal(
            datetime.strptime(
                date_now, '%Y-%m-%d').toordinal() - 10)

        vals = {
            'kosher_ids': [
                (0, 0, {
                    'name': 'Certificate No.2',
                    'date_start': '2016-01-01',
                    'date_end': date_end})
            ]
        }
        product.write(vals)
        self.assertEqual(product.kosher_state, "not_certified")

    def test_product_kosher_status_3(self):
        # CONDITION
        # date_start = True
        # date_end > date.now

        # UPDATE PRODUCT
        criteria = [
            ("id", "=", self.product_3.id)
        ]
        product = self.obj_product_template.search(
            criteria)[0]

        date_now = datetime.now().strftime("%Y-%m-%d")

        date_end = date.fromordinal(
            datetime.strptime(
                date_now, '%Y-%m-%d').toordinal() + 10)

        vals = {
            'kosher_ids': [
                (0, 0, {
                    'name': 'Certificate No.3',
                    'date_start': '2016-11-01',
                    'date_end': date_end})
            ]
        }
        product.write(vals)
        self.assertEqual(product.kosher_state, "certified")
