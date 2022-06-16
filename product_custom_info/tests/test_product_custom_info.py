from odoo.tests.common import Form, TransactionCase


class TestProductCustomInfo(TransactionCase):
    def test_open_product_template(self):
        form = Form(self.env["product.product"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        record = form.save()
        res = record.open_product_template()
        self.assertTrue(res["flags"]["form"]["action_buttons"])

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].new()
