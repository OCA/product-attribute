# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import json

from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductUomReferenceRatio(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.group_ids |= cls.env.ref("uom.group_uom")
        cls.ProductObj = cls.env["product.product"]
        cls.ProductTemplateObj = cls.env["product.template"]
        cls.ProductUomReferenceObj = cls.env["product.uom.reference"]
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_lb = cls.env.ref("uom.product_uom_lb")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_reference_pack = cls.ProductUomReferenceObj.create(
            {
                "name": "Pack 500 g",
                "uom_id": cls.uom_unit.id,
                "uom_reference_id": cls.uom_kg.id,
                "ratio": 0.5,
            }
        )
        cls.product_tmpl = cls.ProductTemplateObj.create(
            {
                "name": "Tomato paste 500 g",
                "type": "consu",
                "list_price": 2.5,
                "uom_id": cls.uom_unit.id,
                "uom_reference_id": cls.uom_reference_pack.id,
            }
        )
        cls.currency = cls.env.company.currency_id

    def create_product_uom_reference(self, equal_reference=False):
        product_uom_reference = self.ProductUomReferenceObj.create(
            {
                "name": "Reference Beef",
                "uom_id": self.uom_kg.id,
                "uom_reference_id": self.uom_kg.id
                if equal_reference
                else self.uom_lb.id,
                "ratio": 2.0,
            }
        )
        return product_uom_reference

    def test_compute_display_name(self):
        product_uom_reference = self.create_product_uom_reference()
        self.assertIn(
            f"[{self.uom_kg.name}-{self.uom_lb.name}]",
            product_uom_reference.display_name,
        )

    def test_check_uom_reference(self):
        with self.assertRaises(ValidationError):
            self.create_product_uom_reference(True)

    def test_configure_uom_reference_in_product(self):
        product_uom_reference = self.create_product_uom_reference()
        product_tmpl_form = Form(
            self.env["product.template"].with_context(
                default_type="consu",
            )
        )
        product_tmpl_form.name = "Beef"
        product_tmpl_form.list_price = 100
        product_tmpl_form.uom_id = self.uom_kg
        product_tmpl_form.uom_reference_id = product_uom_reference
        product_tmpl = product_tmpl_form.save()
        self.assertEqual(product_tmpl.uom_reference_id, product_uom_reference)

    def _render_labels(self, print_format, product_tmpl=None):
        wizard = self.env["product.label.layout"].create(
            {
                "product_tmpl_ids": [(6, 0, (product_tmpl or self.product_tmpl).ids)],
                "custom_quantity": 1,
                "print_format": print_format,
            }
        )
        xml_id, data = wizard._prepare_report_data()
        # The report data goes through JSON in the web client
        data = json.loads(json.dumps(data))
        report = self.env["ir.actions.report"]
        if "zpl" in print_format:
            return str(report._render_qweb_text(xml_id, None, data)[0], "utf-8")
        return str(report._render_qweb_html(xml_id, None, data)[0], "utf-8")

    def test_get_price_uom_reference(self):
        pricelist = self.env["product.pricelist"]
        product = self.product_tmpl.product_variant_id
        self.assertAlmostEqual(
            product._get_price_uom_reference(self.product_tmpl, pricelist), 5.0
        )
        self.product_tmpl.uom_reference_id = False
        self.assertFalse(product._get_price_uom_reference(self.product_tmpl, pricelist))

    def test_pdf_labels_show_price_uom_reference(self):
        for print_format in ("dymo", "2x7xprice", "4x7xprice", "4x12xprice"):
            with self.subTest(print_format=print_format):
                html = self._render_labels(print_format)
                self.assertIn(f"/ {self.uom_unit.name}", html)
                self.assertIn(f"/ {self.uom_kg.name}", html)
                self.assertIn('data-oe-expression="price_uom_reference"', html)
                self.assertIn('<span class="oe_currency_value">5.</span>', html)

    def test_pdf_labels_without_uom_reference(self):
        self.product_tmpl.uom_reference_id = False
        html = self._render_labels("2x7xprice")
        self.assertIn(f"/ {self.uom_unit.name}", html)
        self.assertNotIn(f"/ {self.uom_kg.name}", html)
        self.assertNotIn('data-oe-expression="price_uom_reference"', html)

    def test_zpl_labels_show_price_uom_reference(self):
        zpl = self._render_labels("zplxprice")
        self.assertIn(f"{self.currency.format(2.5)} / {self.uom_unit.name}", zpl)
        self.assertIn(f"( {self.currency.format(5.0)} / {self.uom_kg.name} )", zpl)

    def test_zpl_labels_without_uom_reference(self):
        self.product_tmpl.uom_reference_id = False
        zpl = self._render_labels("zplxprice")
        self.assertNotIn(f"{self.currency.format(2.5)} / {self.uom_unit.name}", zpl)
        self.assertNotIn(f"/ {self.uom_kg.name} )", zpl)
