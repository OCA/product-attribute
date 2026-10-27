# Copyright 2026 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Kévin Roche <kevin.roche@akretion.com>

from odoo.tests import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestProductSupplierinfoIncoterm(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.incoterm_exw = cls.env.ref("account.incoterm_EXW")
        cls.incoterm_dap = cls.env.ref("account.incoterm_DAP")
        cls.vendor_exw = cls.env["res.partner"].create(
            {"name": "Vendor EXW", "purchase_incoterm_id": cls.incoterm_exw.id}
        )
        cls.vendor_dap = cls.env["res.partner"].create(
            {"name": "Vendor DAP", "purchase_incoterm_id": cls.incoterm_dap.id}
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

    def test_incoterm_from_vendor(self):
        supplierinfo = self._create_supplierinfo(self.vendor_exw)
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_exw)

    def test_no_incoterm_on_vendor(self):
        supplierinfo = self._create_supplierinfo(self.vendor_none)
        self.assertFalse(supplierinfo.incoterm_id)

    def test_incoterm_explicit(self):
        supplierinfo = self._create_supplierinfo(
            self.vendor_exw, incoterm_id=self.incoterm_dap.id
        )
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_dap)

    def test_incoterm_follows_vendor_change(self):
        supplierinfo = self._create_supplierinfo(self.vendor_exw)
        supplierinfo.partner_id = self.vendor_dap
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_dap)

    def test_incoterm_from_commercial_partner(self):
        contact = self.env["res.partner"].create(
            {"name": "Contact", "parent_id": self.vendor_dap.id}
        )
        supplierinfo = self._create_supplierinfo(contact)
        self.assertEqual(supplierinfo.incoterm_id, self.incoterm_dap)
