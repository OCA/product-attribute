from odoo.tests import SavepointCase


class TestProductCategory(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductCategory, cls).setUpClass()

        cls.ProductCategory = cls.env["product.category"]
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

    def _get_times(self):
        return ["alert_time", "use_time", "removal_time"]

    def check_field(self, categs, field, name):
        for categ in categs:
            self.assertEqual(
                name,
                getattr(categ, field),
            )
            self.check_field(categ.child_id, field, name)

    def test_modify_root_category(self):
        """
        Test Case:
            Specify a specific_compute_dates_from and specific_alert_time,
            specific_use_time and specific_removal_time at root level
        Expected result:
            The values at all levels must be modified
        """

        self.check_field(self.categ_lvl, "compute_dates_from", "current_date")
        self.categ_lvl.specific_compute_dates_from = "life_date"
        self.check_field(self.categ_lvl, "compute_dates_from", "life_date")
        children = self.categ_lvl.child_id
        self.check_field(children, "compute_dates_from", "life_date")

        for time in self._get_times():
            setattr(self.categ_lvl, "specific_%s" % time, 2)
            children = self.categ_lvl.child_id
            self.check_field(children, time, 2)

    def test_modify_child_category(self):
        """
        Test Case:
            Specify a specific_compute_dates_from and specific_alert_time,
            specific_use_time and specific_removal_time at level_1_1
        Expected result:
            The values at root level and level are the default ("current_date").
            The values at level_1 and level_1_1_1 are the new ones.
        """

        self.check_field(self.categ_lvl, "compute_dates_from", "current_date")
        self.categ_lvl_1_1.specific_compute_dates_from = "life_date"
        self.check_field(self.categ_lvl_1_1, "compute_dates_from", "life_date")
        children = self.categ_lvl_1_1.child_id
        self.check_field(children, "compute_dates_from", "life_date")
        self.assertEqual(self.categ_lvl_1.compute_dates_from, "current_date")
        self.assertEqual(self.categ_lvl.compute_dates_from, "current_date")

        for time in self._get_times():
            setattr(self.categ_lvl_1_1, "specific_%s" % time, 2)
            children = self.categ_lvl_1_1.child_id
            self.check_field(children, time, 2)
            self.assertEqual(getattr(self.categ_lvl, time), 0)
            self.assertEqual(getattr(self.categ_lvl_1, time), 0)
