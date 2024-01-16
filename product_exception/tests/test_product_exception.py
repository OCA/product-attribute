from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductException(TransactionCase):
    def test_product_exception(self):
        exception = self.env.ref("product_exception.excep_no_dump")
        exception.active = True
        p_succ = self.env.ref("product.product_product_7").product_tmpl_id
        p_fail = self.env.ref("product.product_product_6").product_tmpl_id
        self.assertTrue(p_succ.lst_price > p_succ.standard_price)
        self.assertFalse(p_fail.lst_price > p_fail.standard_price)

        self.assertTrue(len(p_succ.exception_ids) == 0)
        self.assertTrue(len(p_fail.exception_ids) == 0)

        prods = p_succ | p_fail
        prods.detect_exceptions()
        self.assertTrue(len(p_succ.exception_ids) == 0)
        self.assertTrue(len(p_fail.exception_ids) == 1)

    def test_check_product_template_cron(self):
        exception = self.env.ref("product_exception.excep_no_dump")
        exception.active = True
        product = self.env.ref("product.product_product_6").product_tmpl_id
        self.assertTrue(len(product.exception_ids) == 0)
        product.check_product_template_cron()
        self.assertTrue(len(product.exception_ids) == 1)

    def test_check_error_raises_on_create_with_field_to_check(self):
        exception = self.env.ref("product_exception.excep_no_dump")
        exception.active = True
        with self.assertRaises(ValidationError):
            self.env["product.template"].with_context(
                test_product_check_exception=True
            ).create(
                {
                    "name": "Test Product",
                    "type": "product",
                    "lst_price": 5,
                    "standard_price": 10,
                    "ignore_exception": False,
                }
            )

    def test_check_error_raises_on_write_with_field_to_check(self):
        exception = self.env.ref("product_exception.excep_no_dump")
        exception.active = True
        product = self.env.ref("product.product_product_6").product_tmpl_id
        with self.assertRaises(ValidationError):
            product.with_context(test_product_check_exception=True).write(
                {"ignore_exception": False, "standard_price": 10000}
            )

    def test_check_skip_error_on_write_with_context(self):
        exception = self.env.ref("product_exception.excep_no_dump")
        exception.active = True
        product = self.env.ref("product.product_product_6").product_tmpl_id
        product.with_context(skip_product_check_exception=True).write(
            {"standard_price": 100}
        )
