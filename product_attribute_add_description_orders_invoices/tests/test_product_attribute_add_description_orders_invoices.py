# Copyright 2022 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tests.common import Form


class TestProductAttributeAddDescriptionOrdersInvoices(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "test_parnter"})
        size_attribute = self.env["product.attribute"].create(
            {
                "name": "Size",
                "display_type": "select",
                "create_variant": "always",
                "show_in_sale_invoices": True,
            }
        )
        size1_value = self.env["product.attribute.value"].create(
            {
                "name": "20x20cm",
                "sequence": 0,
                "display_type": "select",
                "attribute_id": size_attribute.id,
            }
        )
        size2_value = self.env["product.attribute.value"].create(
            {
                "name": "30x30cm",
                "sequence": 1,
                "display_type": "select",
                "attribute_id": size_attribute.id,
            }
        )

        self.product_tmpl = self.env["product.template"].create(
            {
                "name": "T-shirt",
                "type": "consu",
                "categ_id": self.env.ref("product.product_category_all").id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": size_attribute.id,
                            "value_ids": [
                                (4, size1_value.id),
                                (4, size2_value.id),
                            ],
                        },
                    )
                ],
            }
        )
        self.variant_1 = self.product_tmpl.product_variant_ids[0]
        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.variant_1.id,
                            "product_uom_qty": 1,
                            "price_unit": 10.0,
                        },
                    )
                ],
            }
        )
        self.description = "{}\n\n{}".format(
            self.variant_1.display_name, size1_value.display_name
        )

    def test_01_custom_sale_order_description(self):
        line = self.sale_order.order_line[0]
        line.product_id_change()
        self.assertEqual(line.name, self.description, "Incorrect description")

    def test_02_custom_invoice_description(self):
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.partner
        with invoice_form.invoice_line_ids.new() as line:
            line.product_id = self.variant_1
            line.quantity = 1
            line.price_unit = 10.0
        invoice = invoice_form.save()
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.name, self.description, "Incorrect description")
