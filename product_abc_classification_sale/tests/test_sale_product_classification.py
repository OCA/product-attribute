# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from .test_sale_product_classification_common import TestSaleProductClassificationCase


@freeze_time("2021-04-01 00:00:00")
class TestSaleProductClassification(TestSaleProductClassificationCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_sale_order_classification(self):
        """Generate classifications for diferent period slices"""
        # This is the table of expected classifications according to the
        # generated sales depending on the evaluated period:
        # +------------+------+---+------+---+------+---+------+---+------+---+
        # | From date  |  p1  | C |  p2  | C |  p3  | C |  p4  | c |  p5  | C |
        # +------------+------+---+------+---+------+---+------+---+------+---+
        # | 2021-01-01 | 4000 | C | 2000 | D | 6000 | B | 8000 | B | 5000 | B |
        # | 2021-02-01 | 3000 | C |    0 | D | 6000 | B | 8000 | B |    0 | D |
        # | 2021-03-01 | 2000 | D |    0 | D | 3000 | C | 4000 | C |    0 | D |
        # | 2021-04-01 | 1000 | D |    0 | D | 3000 | C | 4000 | C |    0 | D |
        # +------------+------+---+------+---+------+---+------+---+------+---+
        cron_classify = self.env[
            "abc.classification.profile"
        ]._compute_abc_classification
        # We forced the products create date to 2021-03-01, so they won't be
        # evaluated by the cron if set the days to ignore to 365
        self.profile.days_to_ignore = 365
        cron_classify()
        self.assertFalse(any(self.products.mapped("abc_classification_level_id")))
        # Let's reset and now evaluate the a year from now to get all the sales
        # which is the default for sale_classification_days_to_evaluate
        self.profile.days_to_ignore = 0
        cron_classify()
        product_classification = {
            self.prod_1: self.c,
            self.prod_2: self.d,
            self.prod_3: self.b,
            self.prod_4: self.b,
            self.prod_5: self.b,
        }
        self._test_product_classification(product_classification)
        # 70 from now to get sales from february
        self.profile.past_period = 70
        cron_classify()
        product_classification.update({self.prod_5: self.d})
        self._test_product_classification(product_classification)
        # 40 from now to get sales from march
        self.profile.past_period = 40
        cron_classify()
        product_classification.update(
            {self.prod_1: self.d, self.prod_4: self.c, self.prod_3: self.c}
        )
        self._test_product_classification(product_classification)
        # Product 1 gets an A!
        self._create_sale("2021-04-01", self.partner, self.prod_1, 20000)
        cron_classify()
        product_classification.update({self.prod_1: self.a})
        self._test_product_classification(product_classification)
