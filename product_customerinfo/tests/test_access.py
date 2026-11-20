# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestAccess(BaseCommon):
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product = cls.env["product.product"].create({"name": "Test product"})
        cls.vals = {
            "partner_id": cls.partner.id,
            "product_tmpl_id": product.product_tmpl_id.id,
            "price": 80,
        }
        cls.customerinfo = cls.env["product.customerinfo"].create(cls.vals)
        cls.internal_user = new_test_user(
            cls.env, login="customerinfo_internal", groups="base.group_user"
        )
        cls.system_user = new_test_user(
            cls.env, login="customerinfo_system", groups="base.group_system"
        )

    def test_internal_user_reads_only(self):
        customerinfo = self.customerinfo.with_user(self.internal_user)
        self.assertEqual(customerinfo.price, 80)
        with self.assertRaises(AccessError):
            customerinfo.write({"price": 90})
        with self.assertRaises(AccessError):
            customerinfo.create(self.vals)
        with self.assertRaises(AccessError):
            customerinfo.unlink()

    def test_system_user_manages(self):
        customerinfo = self.env["product.customerinfo"].with_user(self.system_user)
        record = customerinfo.create(self.vals)
        record.write({"price": 90})
        self.assertEqual(record.price, 90)
        record.unlink()
