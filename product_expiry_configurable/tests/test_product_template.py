# Copyright 2022 Creu Blanca
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase

from .common import ProductExpiryCategoryCommon


class TestProductTemplate(ProductExpiryCategoryCommon, TransactionCase):
    def test_no_specific_values_set(self):
        """
            Test case:
                  Specify a compute_dates_from, alert_time,
                    use_time and removal_time at the category
                    and not at the product.
        Expected result:
                 The values at the product must be the same that at the category
        """
        self.assertFalse(self.product.use_expiration_date)
        self.categ_lvl_1_1_1.use_expiration_date = True
        self.assertTrue(self.product.use_expiration_date)
        for time in self._get_times():
            self.assertEqual(getattr(self.product, time), 0)
            setattr(self.categ_lvl_1_1_1, "%s" % time, 2)
            self.assertEqual(getattr(self.product, time), 2)

    def test_specific_values_set(self):
        """
            Test case:
                  Specify a compute_dates_from, alert_time,
                    use_time and removal_time at the product.
        Expected result:
                 The values at the product must be different from category's values
        """
        self.assertFalse(self.product.use_expiration_date)
        self.product.use_expiration_date = True
        self.assertTrue(self.product.use_expiration_date)
        for time in self._get_times():
            self.assertEqual(getattr(self.product, time), 0)
            setattr(self.product, "%s" % time, 2)
            self.assertEqual(getattr(self.product, time), 2)
