# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ProductTemplate = self.env["product.template"]
        self.env.ref("base.user_root").write(
            {
                "groups_id": [
                    (4, self.env.ref("uom.group_uom").id),
                ]
            }
        )
        self.volume_both_unit = self.env.ref("uom.product_uom_litre")
        self.volume_sale_unit = self.env.ref("product_uom_use_type.product_uom_pint")
        self.volume_purchase_unit = self.env.ref(
            "product_uom_use_type.product_uom_barrel"
        )
        self.weight_both_unit = self.env.ref("uom.product_uom_kgm")

    def _test_onchange(self, model_name):
        product_form = Form(self.env[model_name])
        product_form.name = "Demo Product"
        product_form.uom_id = self.volume_both_unit
        self.assertEqual(
            product_form.uom_po_id,
            product_form.uom_id,
            "Setting a 'both' unit as main UoM should set the same as Purchase UoM",
        )

        # Change unit to sale unit
        # Should NOT change po_uom_id to the same
        product_form.uom_id = self.volume_sale_unit
        self.assertEqual(
            product_form.uom_po_id,
            self.volume_both_unit,
            "Setting a 'sale' unit as main UoM should not change the purchase UoM",
        )

        # Change unit to sale unit + inconsistent categories
        # Should set uom_po_id to False
        product_form.uom_id = self.weight_both_unit
        product_form.uom_po_id = self.weight_both_unit
        product_form.uom_id = self.volume_sale_unit
        self.assertEqual(
            product_form.uom_po_id.id,
            False,
            "Setting a 'sale' unit as main UoM should set to False the Purchase UoM"
            " if categories doesn't match",
        )

    def test_01_onchange_template(self):
        self._test_onchange("product.template")

    def test_02_onchange_product(self):
        self._test_onchange("product.product")

    def test_03_constrains(self):
        self.ProductTemplate.create(
            {
                "name": "Demo Template OK",
                "uom_id": self.volume_both_unit.id,
                "uom_po_id": self.volume_both_unit.id,
            }
        )

        with self.assertRaises(ValidationError):
            self.ProductTemplate.create(
                {
                    "name": "Demo Template uom_id KO",
                    "uom_id": self.volume_purchase_unit.id,
                    "uom_po_id": self.volume_both_unit.id,
                }
            )

        with self.assertRaises(ValidationError):
            self.ProductTemplate.create(
                {
                    "name": "Demo Template uom_po_id KO",
                    "uom_id": self.volume_both_unit.id,
                    "uom_po_id": self.volume_sale_unit.id,
                }
            )
