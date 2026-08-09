# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT

from ..hooks import pre_init_hook


@tagged("post_install", "-at_install")
class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def _create_variant(self, default_code, categ=None):
        """Return a single variant product carrying ``default_code``.

        The variant is fetched from its template on purpose:
        ``product.product.create()`` returns records bound to a
        ``create_product_product=False`` context, which would prevent the
        copied template from getting a variant at all.
        """
        vals = {"name": "Apple"}
        if categ:
            vals["categ_id"] = categ.id
        template = self.env["product.template"].create(vals)
        variant = template.product_variant_id
        variant.default_code = default_code
        variant.flush_recordset()
        return variant

    def _create_multi_variant_template(self):
        """Return a two variants product in a category with a prefix."""
        attribute = self.env["product.attribute"].create(
            {
                "name": "Color",
                "value_ids": [
                    (0, 0, {"name": "Red"}),
                    (0, 0, {"name": "Blue"}),
                ],
            }
        )
        categ = self.product_category.create(dict(name="Shirts", code_prefix="SHI"))
        template = self.env["product.template"].create(
            {
                "name": "Shirt",
                "categ_id": categ.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, attribute.value_ids.ids)],
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 2)
        return template

    def test_product_copy(self):
        """A copied product gets its own brand new reference."""
        categ = self.product_category.create(dict(name="Fruits", code_prefix="FRU"))
        product_2 = self._create_variant("PROD02", categ)
        copy_product_2 = product_2.copy()
        self.assertEqual(copy_product_2.default_code[:3], "FRU")
        self.assertNotEqual(copy_product_2.default_code, product_2.default_code)

    def test_product_copy_without_default_code(self):
        """A product without reference is copied to a new reference as well."""
        product_2 = self._create_variant(False)
        self.assertFalse(product_2.default_code)
        copy_product_2 = product_2.copy()
        self.assertRegex(copy_product_2.default_code, r"^PR/")

    def test_product_copy_does_not_waste_a_sequence_number(self):
        """Exactly one number is drawn from the sequence per copied product."""
        categ = self.product_category.create(dict(name="Veggies", code_prefix="VEG"))
        product_2 = self._create_variant("/", categ)
        sequence = categ.sequence_id
        before = sequence.number_next_actual
        product_2.copy()
        self.assertEqual(sequence.number_next_actual, before + 1)

    def test_product_copy_with_default_code(self):
        """An explicitly given reference wins over the sequence."""
        categ = self.product_category.create(dict(name="Herbs", code_prefix="HRB"))
        product_2 = self._create_variant("/", categ)
        sequence = categ.sequence_id
        before = sequence.number_next_actual
        copy_product_2 = product_2.copy({"default_code": "PROD02-bis"})
        self.assertEqual(copy_product_2.default_code, "PROD02-bis")
        self.assertEqual(copy_product_2.product_tmpl_id.default_code, "PROD02-bis")
        # No number is drawn from the sequence for a reference nothing uses.
        self.assertEqual(sequence.number_next_actual, before)

    def test_template_copy_with_default_code(self):
        """Same, when the template itself is the one being copied."""
        template = self._create_variant("PROD02").product_tmpl_id
        copy_template = template.copy({"default_code": "PROD02-bis"})
        self.assertEqual(copy_template.default_code, "PROD02-bis")
        self.assertEqual(copy_template.product_variant_id.default_code, "PROD02-bis")

    def test_product_copy_with_slash_default_code(self):
        """Asking for "/" still means "give me a new reference"."""
        categ = self.product_category.create(dict(name="Spices", code_prefix="SPI"))
        product_2 = self._create_variant("/", categ)
        copy_product_2 = product_2.copy({"default_code": "/"})
        self.assertEqual(copy_product_2.default_code[:3], "SPI")
        self.assertNotEqual(copy_product_2.default_code, product_2.default_code)

    def test_multi_variant_copy_with_default_code(self):
        """Variants of a copied product each keep their own reference."""
        template = self._create_multi_variant_template()
        copy_template = template.copy({"default_code": "SHIRT-bis"})
        codes = copy_template.product_variant_ids.mapped("default_code")
        self.assertEqual(len(codes), 2)
        self.assertNotIn("SHIRT-bis", codes)
        self.assertEqual(len(set(codes)), 2, "Variants share the same reference")

    def test_pre_init_hook(self):
        product_3 = self.product_product.create(
            dict(name="Apple", default_code="PROD03")
        )
        self.cr.execute(
            "update product_product set default_code='/' where id=%s",
            (tuple(product_3.ids),),
        )
        product_3.invalidate_recordset()
        self.assertEqual(product_3.default_code, "/")
        pre_init_hook(self.env)
        product_3.invalidate_recordset()
        self.assertEqual(product_3.default_code, f"!!mig!!{product_3.id}")

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

        # Since 19.0 the product category is not mandatory anymore, so a
        # product without category must fall back on the default sequence.
        product_4 = self.product_product.create(
            dict(name="Truck", default_code="PROD04")
        )
        product_4.write({"default_code": "/"})
        self.assertRegex(product_4.default_code, r"^PR/")

        categ_car = self.product_category.create(dict(name="Car", code_prefix="CAR"))
        product_3.product_tmpl_id.categ_id = categ_car
        product_3.product_tmpl_id.default_code = "/"
        product_3.invalidate_recordset()
        self.assertEqual(product_3.default_code[:3], "CAR")
        self.assertEqual(product_3.product_tmpl_id.default_code[:3], "CAR")
        categ_car.write(dict(name="Bike", code_prefix="BIK"))
        self.assertEqual(categ_car.sequence_id.prefix, "BIK")
        categ_car.sequence_id = False
        categ_car.write({"code_prefix": "KIA"})
        self.assertEqual(categ_car.sequence_id.prefix, "KIA")

    def test_product_parent_category_sequence(self):
        # The first half of this test asserts the behaviour when the fallback
        # is disabled, so do not rely on the ambient company setting (the demo
        # data enables it).
        self.env.user.company_id.use_parent_categories_to_determine_prefix = False
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

    def test_product_multi_variant_reference(self):
        """On a multi variant product the reference stays on the variant."""
        template = self._create_multi_variant_template()
        variant, other_variant = template.product_variant_ids
        variant.write({"default_code": "/"})
        self.assertEqual(variant.default_code[:3], "SHI")
        self.assertNotEqual(variant.default_code, other_variant.default_code)
        # The template reference is not overwritten: it is only meaningful
        # when the product has a single variant.
        self.assertFalse(template.default_code)
