# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestFillAttributeLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product_attribute = cls.env["product.attribute"]
        product_attribute_value = cls.env["product.attribute.value"]
        cls.attr_cut = product_attribute.create({"name": "Cut"})
        cls.attr_cut_short = product_attribute_value.create(
            {"name": "Short sleeves", "attribute_id": cls.attr_cut.id}
        )
        cls.attr_cut_long = product_attribute_value.create(
            {"name": "Long sleeves", "attribute_id": cls.attr_cut.id}
        )
        # Not linked to the template, used in test_import_new_value
        cls.attr_cut_tanktop = product_attribute_value.create(
            {"name": "Tanktop", "attribute_id": cls.attr_cut.id}
        )
        # Not linked to the template, used in test_import_new_attr
        cls.attr_embroidery = product_attribute.create({"name": "Embroidery"})
        cls.attr_emb_cheap = product_attribute_value.create(
            {"name": "Cheap", "attribute_id": cls.attr_embroidery.id}
        )
        cls.tmpl = cls.env["product.template"].create(
            {
                "name": "T-shirt",
                "type": "consu",
                "attribute_line_ids": [
                    fields.Command.create(
                        {
                            "attribute_id": cls.attr_cut.id,
                            "value_ids": [
                                fields.Command.set(
                                    [cls.attr_cut_short.id, cls.attr_cut_long.id]
                                )
                            ],
                        }
                    )
                ],
            }
        )

    def _create_product(self, value_ids):
        return self.env["product.product"].create(
            {
                "product_tmpl_id": self.tmpl.id,
                "attribute_value_ids": [fields.Command.set(value_ids)],
            }
        )

    def test_import_existing_product(self):
        """
        - Attribute and Value are already on variant/template
        - Reimport/Create existing variant do nothing
        """
        existing_products = self.tmpl.product_variant_ids
        product = self._create_product([self.attr_cut_long.id])
        self.tmpl.flush_model()
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
