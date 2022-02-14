from odoo.tests import SavepointCase


class TestProductTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductTemplate, cls).setUpClass()

        cls.ProductCategory = cls.env["product.category"]
        cls.ProductProduct = cls.env["product.product"]
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
            {"name": "test product", "categ_id": cls.categ_lvl_1_1_1.id}
        )

    def _get_times(self):
        return ["alert_time", "use_time", "removal_time"]

    def test_no_specific_values_set(self):
        """
            Test case:
                  Specify a compute_dates_from, alert_time,
                    use_time and removal_time at the category
                    and not at the product.
        Expected result:
                 The values at the product must be the same that at the category
        """
        self.assertEqual(self.product.compute_dates_from, "current_date")
        self.categ_lvl_1_1_1.specific_compute_dates_from = "life_date"
        self.assertEqual(self.product.compute_dates_from, "life_date")
        for time in self._get_times():
            self.assertEqual(getattr(self.product, time), 0)
            setattr(self.categ_lvl_1_1_1, "specific_%s" % time, 2)
            self.assertEqual(getattr(self.product, time), 2)

    def test_specific_values_set(self):
        """
            Test case:
                  Specify a compute_dates_from, alert_time,
                    use_time and removal_time at the product.
        Expected result:
                 The values at the product must be different from category's values
        """
        self.assertEqual(self.product.compute_dates_from, "current_date")
        self.product.specific_compute_dates_from = "life_date"
        self.assertEqual(self.product.compute_dates_from, "life_date")
        for time in self._get_times():
            self.assertEqual(getattr(self.product, time), 0)
            setattr(self.product, "specific_%s" % time, 2)
            self.assertEqual(getattr(self.product, time), 2)
