# Copyright (C) 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductSaleTeam(TransactionCase):
    def test_sale_team_field_metadata(self):
        """Ensure product.template has a Many2one to crm.team."""
        ProductTemplate = self.env["product.template"]
        self.assertIn("sales_team_id", ProductTemplate._fields)
        field = ProductTemplate._fields["sales_team_id"]
        self.assertEqual(field.type, "many2one")
        self.assertEqual(field.comodel_name, "crm.team")
