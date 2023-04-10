from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestCommon(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestCommon, self).setUp(*args, **kwargs)

        self.products = self.env["product.product"].create([{"name": "product1"}])

    def test_action_open_product_template(self):
        actual = {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": self.products.product_tmpl_id.id,
            "views": [[False, "form"]],
        }
        expected = self.products.action_open_product_template()
        self.assertDictEqual(expected, actual, msg=None)
