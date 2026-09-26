# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductUomReferenceRatio(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductObj = cls.env["product.product"]
        cls.ProductTemplateObj = cls.env["product.template"]
        cls.ProductUomReferenceObj = cls.env["product.uom.reference"]
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_lb = cls.env.ref("uom.product_uom_lb")

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
