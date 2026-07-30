# Copyright 2023 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.tests import TransactionCase


class TestProductAttributeValueDependentMixinCommon(TransactionCase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ProductSupplierinfoFake

        cls.loader.update_registry((ProductSupplierinfoFake,))

        # Attributs : Taille (S, M, L) et Couleur (Rouge, Bleu)
        cls.attr_size = cls.env["product.attribute"].create({"name": "Size"})
        cls.val_s = cls.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": cls.attr_size.id}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.attr_size.id}
        )
        cls.val_l = cls.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": cls.attr_size.id}
        )
        cls.attr_color = cls.env["product.attribute"].create({"name": "Color"})
        cls.val_red = cls.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": cls.attr_color.id}
        )
        cls.val_blue = cls.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": cls.attr_color.id}
        )

        cls.tmpl_a = cls.env["product.template"].create(
            {
                "name": "Product A",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [(6, 0, [cls.val_s.id, cls.val_m.id])],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_color.id,
                            "value_ids": [(6, 0, [cls.val_red.id, cls.val_blue.id])],
                        },
                    ),
                ],
            }
        )
        cls.variant_a_s_red = cls.tmpl_a.product_variant_ids.filtered(
            lambda p: cls.val_s
            in p.product_template_attribute_value_ids.product_attribute_value_id
            and cls.val_red
            in p.product_template_attribute_value_ids.product_attribute_value_id
        )
        cls.variant_a_m_red = cls.tmpl_a.product_variant_ids.filtered(
            lambda p: cls.val_m
            in p.product_template_attribute_value_ids.product_attribute_value_id
            and cls.val_red
            in p.product_template_attribute_value_ids.product_attribute_value_id
        )
        cls.variant_a_s_blue = cls.tmpl_a.product_variant_ids.filtered(
            lambda p: cls.val_s
            in p.product_template_attribute_value_ids.product_attribute_value_id
            and cls.val_blue
            in p.product_template_attribute_value_ids.product_attribute_value_id
        )

        cls.tmpl_b = cls.env["product.template"].create(
            {
                "name": "Product B",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [(6, 0, [cls.val_s.id])],
                        },
                    ),
                ],
            }
        )
        cls.variant_b_s = cls.tmpl_b.product_variant_ids

        cls.Fake = cls.env["product.supplierinfo.fake"]
        cls.partner = cls.env.ref("base.res_partner_1")

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def _make(self, vals):
        base = {
            "partner_id": self.partner.id,
            "price": 1.0,
            "currency_id": self.env.ref("base.USD").id,
            "min_qty": 1.0,
            "delay": 1,
        }
        base.update(vals)
        return self.Fake.create(base)


class TestProductAttributeValueDependentMixin(
    TestProductAttributeValueDependentMixinCommon
):
    # --- available_product_domain ---

    def test_available_product_domain_with_template(self):
        rec = self._make({"product_tmpl_id": self.tmpl_a.id})
        self.assertEqual(
            rec.available_product_domain,
            [("id", "in", self.tmpl_a.product_variant_ids.ids)],
        )

    def test_available_product_domain_without_template(self):
        rec = self._make({})
        self.assertEqual(rec.available_product_domain, [])

    # --- available_attribute_value_domain ---

    def test_available_attribute_value_domain_with_template(self):
        rec = self._make({"product_tmpl_id": self.tmpl_a.id})
        expected_ids = self.tmpl_a.attribute_line_ids.value_ids.ids
        self.assertEqual(
            rec.available_attribute_value_domain,
            [("id", "in", expected_ids)],
        )

    def test_available_attribute_value_domain_without_template(self):
        rec = self._make({})
        self.assertEqual(rec.available_attribute_value_domain, [])

    # --- is_matching_product ---

    def test_no_criteria_matches_any_product(self):
        rec = self._make({})
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertTrue(rec.is_matching_product(self.variant_b_s))

    def test_product_id_matches_exact_variant(self):
        rec = self._make({"product_id": self.variant_a_s_red.id})
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))

    def test_product_id_rejects_other_variant(self):
        rec = self._make({"product_id": self.variant_a_s_red.id})
        self.assertFalse(rec.is_matching_product(self.variant_a_m_red))

    def test_product_id_takes_precedence_over_attribute_values(self):
        rec = self._make(
            {
                "product_id": self.variant_a_s_red.id,
                "attribute_value_ids": [(6, 0, [self.val_m.id])],
            }
        )
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertFalse(rec.is_matching_product(self.variant_a_m_red))

    def test_tmpl_matches_any_variant_of_template(self):
        rec = self._make({"product_tmpl_id": self.tmpl_a.id})
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertTrue(rec.is_matching_product(self.variant_a_m_red))

    def test_tmpl_rejects_variant_of_other_template(self):
        rec = self._make({"product_tmpl_id": self.tmpl_a.id})
        self.assertFalse(rec.is_matching_product(self.variant_b_s))

    def test_attribute_values_or_within_same_attribute(self):
        rec = self._make(
            {"attribute_value_ids": [(6, 0, [self.val_s.id, self.val_m.id])]}
        )
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertTrue(rec.is_matching_product(self.variant_a_m_red))

    def test_attribute_values_or_within_same_attribute_rejects_l(self):
        rec = self._make({"attribute_value_ids": [(6, 0, [self.val_l.id])]})
        self.assertFalse(rec.is_matching_product(self.variant_a_s_red))

    def test_attribute_values_and_across_attributes(self):
        rec = self._make(
            {"attribute_value_ids": [(6, 0, [self.val_s.id, self.val_red.id])]}
        )
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertFalse(rec.is_matching_product(self.variant_a_m_red))
        self.assertFalse(rec.is_matching_product(self.variant_a_s_blue))

    def test_attribute_values_with_template_rejects_other_template(self):
        rec = self._make(
            {
                "product_tmpl_id": self.tmpl_a.id,
                "attribute_value_ids": [(6, 0, [self.val_s.id])],
            }
        )
        self.assertTrue(rec.is_matching_product(self.variant_a_s_red))
        self.assertTrue(rec.is_matching_product(self.variant_a_s_blue))
        self.assertFalse(rec.is_matching_product(self.variant_b_s))
