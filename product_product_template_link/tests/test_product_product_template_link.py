from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.products = cls.env["product.product"].create([{"name": "product1"}])

    def test_action_open_product_template(self):
        actual = {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": self.products.product_tmpl_id.id,
            "views": [[False, "form"]],
        }
        expected = self.products.action_open_product_template()
        self.assertDictEqual(expected, actual, msg=None)
