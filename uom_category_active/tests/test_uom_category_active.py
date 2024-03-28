# Copyright 2020 Tecnativa - Ernesto Tejeda
# Copyright 2023 PESOL - Angel Moya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestProductCategoryActive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        categ_obj = cls.env["uom.category"]
        cls.uom_categ = categ_obj.create(
            {"name": "Test UoM Category", "uom_ids": [(0, 0, {"name": "Test UoM"})]}
        )

    def test_archive_non_empty_categories(self):
        self.assertTrue(self.uom_categ.active)
        uom = self.uom_categ.uom_ids[0]
        self.assertTrue(uom.active)
        self.uom_categ.active = False
        self.uom_categ._onchange_active()
        self.uom_categ._onchange_uom_ids()
        self.assertFalse(self.uom_categ.active)
        self.assertFalse(uom.active)

    def test_archive_reference_uom(self):
        self.assertTrue(self.uom_categ.active)
        uom = self.uom_categ.uom_ids[0]
        self.assertTrue(uom.active)
        uom.active = False
        with self.assertRaises(UserError):
            self.uom_categ._onchange_uom_ids()
