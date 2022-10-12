from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestSupplierInfo(TransactionCase):
    def setUp(self):
        super(TestSupplierInfo, self).setUp()
        self.partner = self.env["res.partner"].create({"name": "Test partner"})

    def test_product_supplier_infor_for_customer(self):
        form = Form(self.env["product.template"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        with form.customer_ids.new() as line_form:
            line_form.name = self.partner
            line_form.product_name = "ABC"
            line_form.product_code = "CODE"
            line_form.min_qty = 1
            line_form.price = 100
        record = form.save()
        self.assertEqual(len(record.customer_ids), 1)
        line = record.customer_ids[-1]
        self.assertEqual(line.name, self.partner)
        self.assertEqual(line.product_name, "ABC")
        self.assertEqual(line.product_code, "CODE")
        self.assertEqual(line.min_qty, 1)
        self.assertEqual(line.price, 100)
