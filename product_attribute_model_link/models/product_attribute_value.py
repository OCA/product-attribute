# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    linked_record_ref = fields.Reference(
        selection="_selection_target_model", string="Linked record"
    )

    @api.model
    def _selection_target_model(self):
        models = self.env["ir.model"].search_read(
            [("transient", "=", False)], ["model", "name"]
        )
        return [(model["model"], model["name"]) for model in models]

    def convert_attribute_value(self, value, linked_field):
        """
        Convert attribute value name to the appropriate data
        type based on the linked field's type.

        :param value: Value to be converted.
        :return: Converted value or the original value if no conversion is needed.
        """
        if linked_field and linked_field.ttype in ["float", "integer"]:
            return float(value) if linked_field.ttype == "float" else int(value)
        return value

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override to create records based on attribute values.

        :param vals_list: List of dictionaries containing attribute values for creating records.
        :return: Created records.
        :raise: ValidationError if conversion fails for a field.
        """
        product_attribute_obj = self.env["product.attribute"]
        for vals in vals_list:
            attribute_id = (
                vals.get("attribute_id")
                if vals.get("attribute_id")
                else self.env.context.get("default_attribute_id")
            )
            product_attribute = product_attribute_obj.browse(attribute_id)
            # Create new record based on attribute value if create_from_attribute_values is True
            if (
                product_attribute
                and product_attribute.create_from_attribute_values
                and not self.env.context.get("operation_from_record")
            ):
                try:
                    name_value = self.convert_attribute_value(
                        vals["name"], product_attribute.linked_field_id
                    )
                    # Create a new record using the converted or original value
                    new_record = (
                        self.env[product_attribute.linked_model_id.model]
                        .with_context(operation_from_attribute_value=True)
                        .create(
                            {
                                product_attribute.linked_field_id.name: name_value,
                            }
                        )
                    )
                    # Update linked_record_ref with the created record
                    vals["linked_record_ref"] = f"{new_record._name},{new_record.id}"
                except Exception as e:
                    # If conversion fails, raise a ValidationError with details
                    field_name = product_attribute.linked_field_id.name
                    error_message = (
                        f"Conversion failed for the field {field_name}. Error: {e}"
                    )
                    raise ValidationError(
                        _("Validation Error: ") + error_message
                    ) from e
        # Create the records using the super method
        res = super().create(vals_list)
        if self.env.context.get("operation_from_record"):
            return res
        for product_attribute_value in res.filtered(
            "attribute_id.apply_to_products_on_create"
        ):
            # Create related product variants if apply_to_products_on_create is True
            product_template_attribute_lines = (
                self.env["product.template.attribute.line"]
                .search(
                    [
                        (
                            "attribute_id",
                            "=",
                            product_attribute_value.attribute_id.id,
                        )
                    ]
                )
                .with_context(active_test=False)
            )
            product_template_attribute_lines.write(
                {
                    "value_ids": [(4, product_attribute_value.id)],
                }
            )
        return res

    def write(self, vals):
        """
        Override to modify the linked records with given values.

        :param vals: Dictionary of values to be updated.
        :return: Result of the write operation.
        :raise: ValidationError if conversion fails for a field.
        """
        res = super().write(vals)
        # Modify linked record if modify_from_attribute_values is True
        if not self.env.context.get("operation_from_record") and (
            vals.get("name") and not vals.get("linked_record_ref")
        ):
            for product_attribute_value in self.filtered(
                lambda x: x.linked_record_ref
                and x.attribute_id.create_from_attribute_values
                and x.attribute_id.modify_from_attribute_values
            ):
                linked_field = product_attribute_value.attribute_id.linked_field_id
                try:
                    name_value = self.convert_attribute_value(
                        vals["name"], linked_field
                    )
                    product_attribute_value.linked_record_ref.with_context(
                        operation_from_attribute_value=True
                    ).write({linked_field.name: name_value})
                except Exception as e:
                    # If conversion fails, raise a ValidationError with details
                    error_message = (
                        f"Conversion failed for the field {linked_field.name}. "
                        f"Error: {e}"
                    )
                    raise ValidationError(
                        _("Validation Error: ") + error_message
                    ) from e
        return res

    def unlink(self):
        """
        Delete records and associated linked records based on specified conditions.

        :return: Result of the unlink operation.
        """
        for product_attribute_value in self:
            linked_record_ref = product_attribute_value.linked_record_ref
            product_attribute = product_attribute_value.attribute_id
            # Delete linked record if delete_when_attribute_value_is_deleted is True
            if (
                linked_record_ref
                and product_attribute.create_from_attribute_values
                and product_attribute.delete_when_attribute_value_is_deleted
                and not self.env.context.get("operation_from_record")
            ):
                linked_record_ref.with_context(
                    operation_from_attribute_value=True
                ).unlink()
        return super().unlink()

    def action_open_linked_record_wizard(self):
        """
        Action to open a wizard for the linked record.

        :return: Action dictionary to open the wizard.
        """
        self.ensure_one()
        context = {
            "default_linked_record_ref": (
                f"{self.linked_record_ref._name},{self.linked_record_ref.id}"
                if self.linked_record_ref
                else False
            ),
            "default_linked_model": self.attribute_id.linked_model_id.model
            if self.attribute_id.linked_model_id
            else False,
        }
        return {
            "name": "Linked Record Wizard",
            "view_mode": "form",
            "res_model": "linked.record.wizard",
            "view_id": self.env.ref(
                "product_attribute_model_link.view_linked_record_wizard_form"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": context,
        }
