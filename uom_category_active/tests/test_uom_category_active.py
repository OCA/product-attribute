# Copyright 2020 Tecnativa - Ernesto Tejeda
# Copyright 2023 PESOL - Angel Moya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase


class TestProductCategoryActive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        categ_obj = cls.env["uom.category"]
        cls.uom_categ = categ_obj.create(
            {"name": "Test UoM Category", "uom_ids": [(0, 0, {"name": "Test UoM"})]}
        )
        cls.uom = cls.uom_categ.uom_ids[0]

    def test_archive_non_empty_categories(self):
        self.assertTrue(self.uom_categ.active)
        self.assertTrue(self.uom.active)
        self.uom_categ.active = False
        self.assertFalse(self.uom_categ.active)
        self.assertFalse(self.uom.active)
