# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductCategoryPricelistButton(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env["product.category"].create({"name": "Test Category"})

    def test_action_view_pricelists(self):
        action = self.category.action_view_pricelists()

        self.assertEqual(action.get("type"), "ir.actions.act_window")
        self.assertEqual(action.get("res_model"), "product.pricelist.item")
        self.assertEqual(action.get("domain"), [("categ_id", "in", self.category.ids)])
        self.assertEqual(action.get("target"), "current")
