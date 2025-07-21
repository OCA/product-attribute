from odoo import Command
from odoo.tests import Form, RecordCapturer, tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestSaleProductMatrixSecondaryUnit(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure the UoM group is enabled
        config = Form(cls.env["res.config.settings"])
        config.group_uom = True
        config = config.save()
        config.execute()
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.attribute1 = cls.env["product.attribute"].create(
            {"name": "SecUnit 1", "create_variant": "always", "sequence": 1}
        )
        cls.attribute2 = cls.env["product.attribute"].create(
            {"name": "SecUnit 2", "create_variant": "always", "sequence": 2}
        )
        cls.attribute_value1 = cls.env["product.attribute.value"].create(
            [{"name": "SecUnitVal 1", "attribute_id": cls.attribute1.id}]
        )
        cls.attribute_value2 = cls.env["product.attribute.value"].create(
            [{"name": "SecUnitVal 2", "attribute_id": cls.attribute1.id}]
        )
        cls.attribute_value3 = cls.env["product.attribute.value"].create(
            [{"name": "SecUnitVal 3", "attribute_id": cls.attribute2.id}]
        )
        cls.attribute_value4 = cls.env["product.attribute.value"].create(
            [{"name": "SecUnitVal 4", "attribute_id": cls.attribute2.id}]
        )
        cls.matrix_template = cls.env["product.template"].create(
            {
                "name": "SecondaryUnitMatrix",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "product_add_mode": "matrix",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attribute1.id,
                            "value_ids": [(6, 0, cls.attribute1.value_ids.ids)],
                        },
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.attribute2.id,
                            "value_ids": [(6, 0, cls.attribute2.value_ids.ids)],
                        },
                    ),
                ],
            }
        )

    def test_sale_matrix_with_secondary_unit(self):
        # Set the template as configurable by matrix.
        SecondaryUnit = self.env["product.secondary.unit"]
        secondary_unit_1 = SecondaryUnit.create(
            {
                "name": "Unit 1",
                "product_tmpl_id": self.matrix_template.id,
                "uom_id": self.uom_unit.id,
                "factor": 12.0,
            }
        )
        with RecordCapturer(self.env["sale.order"], []) as capture:
            self.start_tour("/web", "sale_matrix_with_secondary_unit", login="admin")
        new_sale = capture.records
        # Ensures a SO has been created with exactly 4 lines
        self.assertEqual(len(new_sale.order_line), 4)
        self.assertEqual(new_sale.order_line[0].secondary_uom_id, secondary_unit_1)
        self.assertEqual(new_sale.order_line[0].secondary_uom_qty, 1)
        self.assertEqual(new_sale.order_line[0].product_uom_qty, 12)
        self.assertEqual(new_sale.order_line[1].secondary_uom_id, secondary_unit_1)
        self.assertEqual(new_sale.order_line[1].secondary_uom_qty, 1)
        self.assertEqual(new_sale.order_line[1].product_uom_qty, 12)
        self.assertEqual(new_sale.order_line[2].secondary_uom_id, secondary_unit_1)
        self.assertEqual(new_sale.order_line[2].secondary_uom_qty, 1)
        self.assertEqual(new_sale.order_line[2].product_uom_qty, 12)
        self.assertEqual(new_sale.order_line[3].secondary_uom_id, secondary_unit_1)
        self.assertEqual(new_sale.order_line[3].secondary_uom_qty, 1)
        self.assertEqual(new_sale.order_line[3].product_uom_qty, 12)

    def test_sale_matrix_without_secondary_unit(self):
        with RecordCapturer(self.env["sale.order"], []) as capture:
            self.start_tour("/web", "sale_matrix_without_secondary_unit", login="admin")
        new_sale = capture.records
        # Ensures a SO has been created with exactly 4 lines
        self.assertEqual(len(new_sale.order_line), 4)
        self.assertFalse(new_sale.order_line[0].secondary_uom_id)
        self.assertEqual(new_sale.order_line[0].secondary_uom_qty, 0)
        self.assertEqual(new_sale.order_line[0].product_uom_qty, 1)
        self.assertFalse(new_sale.order_line[1].secondary_uom_id)
        self.assertEqual(new_sale.order_line[1].secondary_uom_qty, 0)
        self.assertEqual(new_sale.order_line[1].product_uom_qty, 1)
        self.assertFalse(new_sale.order_line[2].secondary_uom_id)
        self.assertEqual(new_sale.order_line[2].secondary_uom_qty, 0)
        self.assertEqual(new_sale.order_line[2].product_uom_qty, 1)
        self.assertFalse(new_sale.order_line[3].secondary_uom_id)
        self.assertEqual(new_sale.order_line[3].secondary_uom_qty, 0)
        self.assertEqual(new_sale.order_line[3].product_uom_qty, 1)
