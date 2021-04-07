# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestProductCategoryCode(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        vals = {
            "name": "Category Test",
            "code": "TEST",
        }
        cls.category = cls.env["product.category"].create(vals)

    def test_category(self):
        new_category = self.category.copy()

        self.assertEqual(
            "TEST-copy",
            new_category.code,
        )
