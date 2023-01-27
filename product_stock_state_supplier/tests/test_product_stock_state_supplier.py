# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestProductStockState(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_threshold_on_product = cls.env.ref(
            "product_stock_state.product_setting_by_product"
        )
        cls.supplierinfo = cls.env["product.supplierinfo"].create(
            {
                "name": cls.env.ref("base.res_partner_1").id,
                "product_tmpl_id": cls.product_threshold_on_product.product_tmpl_id.id,
            }
        )

    def test_state_resupplyable(self):
        """Test Stock State computation"""
        self.supplierinfo.write({"supplier_quantity": 100})
        self.assertEqual(self.product_threshold_on_product.stock_state, "resupplyable")
