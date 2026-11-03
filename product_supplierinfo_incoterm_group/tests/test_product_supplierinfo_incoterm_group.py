# Copyright 2026 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Kévin Roche <kevin.roche@akretion.com>

from odoo.tests import TransactionCase


class TestProductSupplierinfoIncotermGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.incoterm_exw = cls.env.ref("account.incoterm_EXW")
        cls.incoterm_dap = cls.env.ref("account.incoterm_DAP")
        cls.vendor = cls.env["res.partner"].create(
            {"name": "Vendor", "purchase_incoterm_id": cls.incoterm_exw.id}
        )
        cls.vendor_none = cls.env["res.partner"].create({"name": "Vendor None"})
        cls.product_tmpl = cls.env["product.template"].create({"name": "Product"})

    def _create_supplierinfo(self, partner, **kwargs):
        vals = {
            "partner_id": partner.id,
            "product_tmpl_id": self.product_tmpl.id,
            "price": 10.0,
        }
        vals.update(kwargs)
        return self.env["product.supplierinfo"].create(vals)

    def test_group_incoterm_from_vendor(self):
        supplierinfo = self._create_supplierinfo(self.vendor)
        self.assertEqual(supplierinfo.group_id.incoterm_id, self.incoterm_exw)
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_exw)

    def test_group_without_incoterm(self):
        supplierinfo = self._create_supplierinfo(self.vendor_none)
        self.assertFalse(supplierinfo.group_id.incoterm_id)
        self.assertFalse(supplierinfo.incoterm_id)

    def test_same_incoterm_same_group(self):
        supplierinfo_1 = self._create_supplierinfo(self.vendor, min_qty=1)
        supplierinfo_2 = self._create_supplierinfo(self.vendor, min_qty=10)
        self.assertEqual(supplierinfo_1.group_id, supplierinfo_2.group_id)

    def test_other_incoterm_other_group(self):
        supplierinfo_exw = self._create_supplierinfo(self.vendor)
        supplierinfo_dap = self._create_supplierinfo(
            self.vendor, incoterm_id=self.incoterm_dap.id, price=11.5
        )
        self.assertNotEqual(supplierinfo_exw.group_id, supplierinfo_dap.group_id)
        self.assertEqual(supplierinfo_exw.incoterm_id, self.incoterm_exw)
        self.assertEqual(supplierinfo_dap.incoterm_id, self.incoterm_dap)
        self.assertEqual(supplierinfo_dap.group_id.incoterm_id, self.incoterm_dap)

    def test_group_incoterm_propagated_to_supplierinfo(self):
        supplierinfo = self._create_supplierinfo(self.vendor)
        supplierinfo.group_id.incoterm_id = self.incoterm_dap
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_dap)

    def test_group_incoterm_follows_vendor(self):
        group = self.env["product.supplierinfo.group"].create(
            {"product_tmpl_id": self.product_tmpl.id, "partner_id": self.vendor.id}
        )
        self.assertEqual(group.incoterm_id, self.incoterm_exw)
        group.partner_id = self.vendor_none
        self.assertFalse(group.incoterm_id)
