# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from os import path

PATH = path.dirname(__file__) + "/fixtures/"


class TestVariantAttrToTmpl(TransactionCase):
    def get_csv_file(self, filename):
        return open(PATH + filename).read()

    def load_csv(self, filename):
        import_wizard = self.env["base_import.import"].create(
            {
                "res_model": "product.product",
                "file": self.get_csv_file(filename),
                "file_type": "text/csv",
            }
        )
        data, fields = import_wizard._convert_import_data(
            ["id", "attribute_value_ids/id", "product_tmpl_id/id"],
            {"quoting": '"', "separator": ",", "headers": True},
        )
        self.env["product.product"].load(fields, data)

    def setUp(self):
        super().setUp()
        self.tmpl = self.env.ref(
            "product_import_autocomplete_attribute." "demo_product_tmpl_tshirt"
        )
        self.attr_line_cuts = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_template_attribute_line_cut"
        )
        self.attr_cut_tanktop = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_cut_tanktop"
        )
        self.attr_emb = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_embroidery"
        )
        self.attr_emb_cheap = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_embroidery_cheap"
        )
        self.attr_emb_hq = self.env.ref(
            "product_import_autocomplete_attribute."
            "demo_product_attribute_embroidery_hq"
        )

    def test_import_same_attr_new_value(self):
        """
        - Attribute is already on variant/template
        - Import new attribute value on variant
        """
        self.load_csv("new_value_cut_tanktop.csv")
        self.assertIn(self.attr_cut_tanktop, self.attr_line_cuts.value_ids)

    def test_import_new_attr(self):
        """
        - Attribute is not yet on variant/template
        - Import new attribute value (on new variant)
        """
        self.load_csv("new_attr_embroidery_cheap.csv")
        new_attr_line = self.tmpl.attribute_line_ids.filtered(
            lambda r: r.attribute_id == self.attr_emb
        )
        self.assertTrue(new_attr_line)
        self.assertIn(self.attr_emb_cheap, new_attr_line.value_ids)

    def test_import_new_attrs_different_variant(self):
        """
        - Attribute is not yet on variant/template
        - Import 2 new attribute value (on 2 new different variants)
        """
        self.load_csv("new_attrs_embroidery_all.csv")
        new_attr_line = self.tmpl.attribute_line_ids.filtered(
            lambda r: r.attribute_id == self.attr_emb
        )
        self.assertIn(self.attr_emb_cheap, new_attr_line.mapped("value_ids"))
        self.assertIn(self.attr_emb_hq, new_attr_line.mapped("value_ids"))

    def test_import_different_attrs_different_variant(self):
        """
        - Attributes "cut" is on variant/template, "embroidery" isn't
        - Import 2 new, different attribute values on the same variant
        """
        self.load_csv("new_attrs_embroidery_cut.csv")
        self.assertIn(self.attr_cut_tanktop, self.attr_line_cuts.value_ids)
        attr_line_cut = self.tmpl.attribute_line_ids.filtered(
            lambda r: r.attribute_id == self.attr_emb
        )
        self.assertIn(self.attr_emb_cheap, attr_line_cut.mapped("value_ids"))

    def test_no_useless_variants_created(self):
        """
        - Check readme for description of example imports, this is the same
        - Import combined CSV file from examples folder
        - 3 attribute values from "Embroidery", 3 attribute values from "Cut"
        - We would get 3*3 variants normally
        - Test we don't get the other useless variants
        """
        self.load_csv("test_useless_variants.csv")
        self.assertEqual(len(self.tmpl.product_variant_ids.ids), 3)
