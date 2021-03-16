# © 2020 TestVariantAttrToTmplAkretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestFillAttributeLine(TransactionCase):
    def _create_product(self, value_ids):
        return self.env["product.product"].create({
            "product_tmpl_id": self.tmpl.id,
            "attribute_value_ids": [(6, 0, value_ids)],
            })

    def setUp(self):
        super().setUp()
        self.tmpl = self.env.ref(
            "product_import_autocomplete_attribute.demo_product_tmpl_tshirt"
        )
        self.attr_cut_tanktop = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_cut_tanktop"
        )
        self.attr_cut_long = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_cut_long"
        )
        self.attr_emb_cheap = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_embroidery_cheap"
        )

    def test_import_existing_product(self):
        """
        - Attribute and Value are already on variant/template
        - Reimport/Create existing variant do nothing
        """
        existing_products = self.tmpl.product_variant_ids
        product = self._create_product([self.attr_cut_long.id])
        self.tmpl.flush()
        self.assertIn(product, existing_products)
        self.assertEqual(existing_products, self.tmpl.product_variant_ids)

    def test_import_new_attr(self):
        """
        - Attribute is not yet on variant/template
        - Import new attribute value (on new variant)
        """
        value_ids = [self.attr_emb_cheap.id, self.attr_cut_long.id]
        self._create_product(value_ids)
        self.assertEqual(len(self.tmpl.attribute_line_ids), 2)
        variants = self.tmpl.with_context(active_test=False).product_variant_ids
        self.assertEqual(len(variants), 2)
        self.assertEqual(variants[1].attribute_value_ids.ids, value_ids)

    def test_import_new_value(self):
        self._create_product([self.attr_cut_tanktop.id])
        self.assertEqual(len(self.tmpl.attribute_line_ids), 1)
        self.assertEqual(len(self.tmpl.product_variant_ids), 3)

    def test_incoherent_new_attr(self):
        with self.assertRaises(UserError):
            self._create_product([self.attr_emb_cheap.id])
