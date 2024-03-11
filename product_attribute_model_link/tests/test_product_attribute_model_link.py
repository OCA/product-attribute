# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import Command
from odoo.tests import TransactionCase


class TestProductAttributeModelLink(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.env.registry.ready = True
        # Setup Material model
        cls.material_model = cls.env["ir.model"].create(
            {
                "name": "Material",
                "model": "x_material_model",
                "field_id": [
                    Command.create(
                        {"name": "x_name", "ttype": "char", "field_description": "Name"}
                    )
                ],
            }
        )

        cls.material_field = cls.env["ir.model.fields"].create(
            {
                "name": "x_description",
                "model_id": cls.material_model.id,
                "field_description": "Description",
                "ttype": "char",
            }
        )

        cls.material_attribute = cls.env["product.attribute"].create(
            {
                "name": "Material Attribute",
                "linked_model_id": cls.material_model.id,
                "linked_field_id": cls.material_field.id,
                "domain": "[('x_name','like', 'Material 1')]",
                "create_from_attribute_values": True,
                "modify_from_attribute_values": True,
                "delete_when_attribute_value_is_deleted": True,
                "apply_to_products_on_create": True,
            }
        )

    def test_create_record(self):
        # Test creating a record in the Material model
        material_record = self.env["x_material_model"].create(
            {
                "x_name": "Material 1",
                "x_description": "Cotton",
            }
        )

        self.assertTrue(material_record, "Material Record not created")

        # Check if linked attribute value record is created
        material_attribute_value = self.env["product.attribute.value"].search(
            [("name", "=", "Cotton"), ("attribute_id", "=", self.material_attribute.id)]
        )
        self.assertTrue(material_attribute_value, "Linked attribute value not created")
        self.assertEqual(
            material_record.id,
            material_attribute_value.linked_record_ref.id,
            "Linked record ref is wrong!",
        )

        material_record = self.env["x_material_model"].create(
            {
                "x_name": "Material 2",
                "x_description": "Wool",
            }
        )

        self.assertTrue(material_record, "Material Record not created")

        # Because of the domain, there should be no linked attribute value
        material_attribute_value = self.env["product.attribute.value"].search(
            [("name", "=", "Wool"), ("attribute_id", "=", self.material_attribute.id)]
        )
        self.assertFalse(material_attribute_value, "Linked attribute value created")

    def test_edit_linked_record(self):
        # Test editing a linked record and check if linked attribute value updates
        material_record = self.env["x_material_model"].create(
            {
                "x_name": "Material 1",
                "x_description": "Cotton",
            }
        )

        material_attribute_value = self.env["product.attribute.value"].search(
            [
                ("name", "=", "Cotton"),
                ("attribute_id", "=", self.material_attribute.id),
            ],
            limit=1,
        )

        # Edit the material record directly
        material_record.write(
            {
                "x_description": "Silk",
            }
        )

        # Check if the linked attribute value reflects the change
        self.assertEqual(
            material_attribute_value.name, "Silk", "Linked field not updated"
        )

    def test_delete_linked_record(self):
        # Test deleting a linked record and check if linked attribute value is deleted
        material_record = self.env["x_material_model"].create(
            {
                "x_name": "Material 1",
                "x_description": "Cotton",
            }
        )

        material_attribute_value = self.env["product.attribute.value"].search(
            [
                ("name", "=", "Cotton"),
                ("attribute_id", "=", self.material_attribute.id),
            ],
            limit=1,
        )

        # Delete the material record directly
        material_record.unlink()

        material_attribute_value = self.env["product.attribute.value"].browse(
            material_attribute_value.id
        )

        # Check if the linked attribute value is also deleted
        self.assertFalse(
            material_attribute_value.exists(), "Linked attribute value not deleted"
        )

    def test_apply_to_products_on_create(self):
        # Simulate creation of an attribute value and verify its application to products
        material_cotton_attribute_value = self.env["product.attribute.value"].create(
            {
                "name": "Cotton",
                "attribute_id": self.material_attribute.id,
            }
        )

        test_template = self.env["product.template"].create(
            {
                "name": "Sofa",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.material_attribute.id,
                            "value_ids": [
                                Command.link(material_cotton_attribute_value.id)
                            ],
                        }
                    ),
                ],
            }
        )
        material_silk_attribute_value = self.env["product.attribute.value"].create(
            {
                "name": "Silk",
                "attribute_id": self.material_attribute.id,
            }
        )

        product_template_attribute_line = self.env[
            "product.template.attribute.line"
        ].search(
            [
                (
                    "attribute_id",
                    "=",
                    self.material_attribute.id,
                ),
                (
                    "product_tmpl_id",
                    "=",
                    test_template.id,
                ),
            ]
        )

        self.assertIn(
            material_silk_attribute_value.id,
            product_template_attribute_line.value_ids.ids,
            "Attribute Value not applied to the Product",
        )

    def test_create_from_attribute_values(self):
        # Simulate creation of an attribute value and check if it
        # creates a record in the linked model
        product_attribute_value = self.env["product.attribute.value"].create(
            {
                "name": "Silk",
                "attribute_id": self.material_attribute.id,
            }
        )

        # Check if a record in the linked model was created
        linked_model_record = self.env["x_material_model"].search(
            [("x_description", "=", "Silk")]
        )
        self.assertTrue(linked_model_record, "Linked model record not created!")
        self.assertEqual(
            linked_model_record.id,
            product_attribute_value.linked_record_ref.id,
            "Linked record ref is wrong!",
        )

    def test_modify_from_attribute_values(self):
        # Simulate modifying an attribute value and
        # check if it updates the linked model's record
        material_attribute_value = self.env["product.attribute.value"].create(
            {
                "name": "Wool",
                "attribute_id": self.material_attribute.id,
            }
        )

        # Modify the attribute value
        material_attribute_value.write({"name": "Cashmere"})

        # Check if the linked model's record was updated
        linked_model_record = self.env["x_material_model"].search(
            [
                ("x_description", "=", "Cashmere"),
                ("id", "=", material_attribute_value.linked_record_ref.id),
            ]
        )
        self.assertTrue(linked_model_record, "Linked model record not updated")

    def test_delete_when_attribute_value_is_deleted(self):
        # Simulate deletion of an attribute value and
        # verify if the linked model's record is deleted
        material_attribute_value = self.env["product.attribute.value"].create(
            {
                "name": "Polyester",
                "attribute_id": self.material_attribute.id,
            }
        )

        # Delete the attribute value
        material_attribute_value.unlink()

        # Check if the linked model's record was also deleted
        linked_model_record = self.env["x_material_model"].search(
            [("x_description", "=", "Polyester")]
        )
        self.assertFalse(linked_model_record, "Linked model record not deleted")
