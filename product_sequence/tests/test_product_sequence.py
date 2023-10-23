# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged

from ..hooks import pre_init_hook


@tagged("post_install", "-at_install")
class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    @classmethod
    def setUpClass(cls):
        super(TestProductSequence, cls).setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.product_product = cls.env["product.product"]
        cls.product_category = cls.env["product.category"]
        cls.product_template = cls.env["product.template"].create(
            {"name": "Demo Product"}
        )

    def test_product_create_with_default_code(self):
        product = self.product_product.create(dict(name="Apple", default_code="PROD01"))
        self.assertEqual(product.default_code, "PROD01")
        product_new = self.product_product.create(
            dict(name="Demo Apple", product_tmpl_id=self.product_template.id)
        )
        self.assertTrue(product_new.default_code)

    def test_product_create_without_default_code(self):
        product_1 = self.product_product.create(dict(name="Orange", default_code="/"))
        self.assertRegex(str(product_1.default_code), r"PR/*")

    def test_product_copy(self):
        product_2 = self.product_template.create(
            dict(name="Apple", default_code="PROD02")
        )
        product_2.flush()
        copy_product_2 = product_2.product_variant_id.copy()
        self.assertEqual(copy_product_2.default_code, "PROD02-copy")

    def test_pre_init_hook(self):
        product_3 = self.product_product.create(
            dict(name="Apple", default_code="PROD03")
        )
        self.cr.execute(
            "update product_product set default_code='/' where id=%s",
            (tuple(product_3.ids),),
        )
        product_3.invalidate_cache()
        self.assertEqual(product_3.default_code, "/")
        pre_init_hook(self.cr)
        product_3.invalidate_cache()
        self.assertEqual(product_3.default_code, "!!mig!!{}".format(product_3.id))

    def test_product_category_sequence(self):
        categ_grocery = self.product_category.create(
            dict(name="Grocery", code_prefix="GRO")
        )
        self.assertTrue(categ_grocery.sequence_id)
        self.assertEqual(categ_grocery.sequence_id.prefix, "GRO")
        self.assertFalse(categ_grocery.sequence_id.company_id)
        product_3 = self.product_product.create(
            dict(name="Apple", categ_id=categ_grocery.id)
        )
        self.assertEqual(product_3.default_code[:3], "GRO")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "GRO")
        categ_electronics = self.product_category.create(
            dict(name="Electronics", code_prefix="ELE")
        )
        product_3.write({"default_code": "/", "categ_id": categ_electronics.id})
        self.assertEqual(product_3.default_code[:3], "ELE")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "ELE")

        product_4 = self.product_product.create(
            dict(name="Truck", default_code="PROD04")
        )
        product_4.write({"default_code": "/"})
        self.assertTrue(product_4.categ_id, "Category is not set.")

        categ_car = self.product_category.create(dict(name="Car", code_prefix="CAR"))
        product_3.product_tmpl_id.categ_id = categ_car
        product_3.product_tmpl_id.default_code = "/"
        product_3.refresh()
        self.assertEqual(product_3.default_code[:3], "CAR")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "CAR")
        categ_car.write(dict(name="Bike", code_prefix="BIK"))
        self.assertEqual(categ_car.sequence_id.prefix, "BIK")
        categ_car.sequence_id = False
        categ_car.write({"code_prefix": "KIA"})
        self.assertEqual(categ_car.sequence_id.prefix, "KIA")

    def test_product_parent_category_sequence(self):
        parent_categ = self.product_category.create(
            dict(
                name="Parents",
                code_prefix="PAR",
            )
        )
        categ = self.product_category.create(
            dict(
                name="Child",
                parent_id=parent_categ.id,
            )
        )

        product_anna = self.product_product.create(
            dict(
                name="Anna",
                categ_id=categ.id,
            )
        )
        self.assertEqual(product_anna.default_code[:2], "PR")
        self.assertEqual(product_anna.product_tmpl_id.default_code[:2], "PR")

        self.env.user.company_id.use_parent_categories_to_determine_prefix = True

        product_claudia = self.product_product.create(
            dict(
                name="Claudia",
                categ_id=categ.id,
            )
        )
        self.assertEqual(product_claudia.default_code[:3], "PAR")
        self.assertEqual(product_claudia.product_tmpl_id.default_code[:3], "PAR")

    def test_product_copy_with_default_values(self):
        product_2 = self.product_template.create(
            dict(name="Apple", default_code="PROD02")
        )
        product_2.flush()
        copy_product_2 = product_2.product_variant_id.copy(
            {"default_code": "product test sequence"}
        )
        self.assertEqual(copy_product_2.default_code, "product test sequence")

    def test_remove_and_reuse_sequence(self):
        prefix = "TEST"
        category = self.product_category.create({"name": "Test", "code_prefix": prefix})
        test_sequence = category.sequence_id
        self.assertTrue(test_sequence)
        self.assertEqual(test_sequence.prefix, prefix)
        category.write({"code_prefix": ""})
        self.assertFalse(category.sequence_id)
        category.write({"code_prefix": prefix})
        self.assertEqual(category.sequence_id, test_sequence)
        category_2 = self.product_category.create(
            {"name": "Test reuse", "code_prefix": prefix}
        )
        self.assertEqual(category_2.sequence_id, test_sequence)

    def test_sequence_prefix_discrepancies(self):
        prefix_test = "TEST"
        category_test = self.product_category.create(
            {"name": "Test", "code_prefix": prefix_test}
        )
        sequence_test = category_test.sequence_id
        prefix_demo = "DEMO"
        category_demo = self.product_category.create(
            {"name": "Demo", "code_prefix": prefix_demo}
        )
        with self.assertRaisesRegex(
            ValidationError, "prefix defined on product category"
        ):
            category_demo.sequence_id = sequence_test
        with self.assertRaisesRegex(
            ValidationError, "used on following product categories"
        ):
            sequence_test.prefix = prefix_demo
