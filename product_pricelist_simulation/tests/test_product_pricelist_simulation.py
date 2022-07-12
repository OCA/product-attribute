# Copyright 2017 Tecnativa - Sergio Teruel
# Copyright 2022 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common


class TestProductPricelistSimulation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template_1 = cls.env["product.template"].create(
            {"name": "Template 1", "list_price": 100.00}
        )
        attr = cls.env["product.attribute"].create({"name": "Attr"})
        attr_value_1 = cls.env["product.attribute.value"].create(
            {"name": "Value 1", "attribute_id": attr.id},
        )
        attr_value_2 = cls.env["product.attribute.value"].create(
            {"name": "Value 2", "attribute_id": attr.id},
        )
        cls.template_2 = cls.env["product.template"].create(
            {
                "name": "Template 2",
                "list_price": 1000.00,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr.id,
                            "value_ids": [(6, 0, [attr_value_1.id, attr_value_2.id])],
                        },
                    )
                ],
            }
        )
        # uncheck 'show_in_simulation' in existing pricelist (just in case)
        cls.env["product.pricelist"].search([]).show_in_simulation = False
        cls.pricelist_1 = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist 1",
                "currency_id": cls.env.company.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "fixed",
                            "fixed_price": 80.00,
                        },
                    )
                ],
            }
        )
        cls.pricelist_2 = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist 2",
                "currency_id": cls.env.company.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "percentage",
                            "percent_price": 50.00,
                        },
                    )
                ],
            }
        )
        cls.pricelist_3 = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist3",
                "currency_id": cls.env.company.currency_id.id,
                "show_in_simulation": False,
            }
        )

    def test_pricelist_simulation_product_template(self):
        # # Template 1
        wizard_form = Form(
            self.env["wizard.preview.pricelist"].with_context(
                active_model="product.template", active_id=self.template_1.id,
            ),
        )
        self.assertAlmostEqual(wizard_form.line_ids._records[0]["price"], 50.0)
        self.assertAlmostEqual(wizard_form.line_ids._records[1]["price"], 80.0)
        # # Template 2
        wizard_form = Form(
            self.env["wizard.preview.pricelist"].with_context(
                active_model="product.template", active_id=self.template_2.id,
            ),
        )
        prices = [r["price"] for r in wizard_form.line_ids._records]
        self.assertAlmostEqual(prices, [500.0, 80.0, 500.0, 80.0])

    def test_pricelist_simulation_product_variant(self):
        wizard_form = Form(
            self.env["wizard.preview.pricelist"].with_context(
                active_model="product.product",
                active_id=self.template_1.product_variant_ids.id,
            ),
        )
        self.assertAlmostEqual(wizard_form.line_ids._records[0]["price"], 50.0)
        self.assertAlmostEqual(wizard_form.line_ids._records[1]["price"], 80.0)
