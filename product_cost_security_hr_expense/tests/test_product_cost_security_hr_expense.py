# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductCostSecurityHrExpense(BaseCommon):
    def test_expense_form_view_has_no_access_rights_warning(self):
        """The restricted cost field must not leak into unrestricted elements."""
        view = self.env.ref("hr_expense.product_product_expense_form_view")
        self.assertNotIn("standard_price", view.warning_info)
