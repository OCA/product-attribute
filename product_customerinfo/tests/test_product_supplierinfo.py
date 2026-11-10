# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.base.tests.common import BaseCommon


class TestProductSupplierinfo(BaseCommon):
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["product.template"].create({"name": "Test product"})
        values = {"product_tmpl_id": cls.template.id}
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier"})
        cls.customer = cls.env["res.partner"].create({"name": "Customer"})
        cls.supplierinfo = cls.env["product.supplierinfo"].create(
            {**values, "partner_id": cls.supplier.id, "price": 10.0}
        )
        cls.customerinfo = cls.env["product.customerinfo"].create(
            {**values, "partner_id": cls.customer.id, "price": 20.0}
        )
        cls.domain = [("product_tmpl_id", "=", cls.template.id)]

    def test_read_without_customerinfo_context(self):
        data = self.supplierinfo.read(["price"])
        self.assertEqual([x["price"] for x in data], [10.0])

    def test_search_fetch_adds_the_customerinfo(self):
        infos = self.env["product.supplierinfo"].search_fetch(self.domain, ["price"])
        self.assertEqual(len(infos), 1)
        infos = self.env["product.supplierinfo"].with_context(customerinfo=True)
        infos = infos.search_fetch(self.domain, ["price"], limit=5)
        self.assertEqual(sorted(infos.mapped("price")), [10.0, 20.0])

    def test_read_with_customerinfo_context(self):
        infos = self.env["product.supplierinfo"].with_context(customerinfo=True)
        infos = infos.search_fetch(self.domain, ["price"])
        data = infos.read(["price", "partner_id"])
        self.assertEqual(sorted(x["price"] for x in data), [10.0, 20.0])
        data = infos.read()
        self.assertEqual(len(data), 2)
