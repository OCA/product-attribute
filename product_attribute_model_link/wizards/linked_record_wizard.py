# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class LinkedRecordWizard(models.TransientModel):
    _name = "linked.record.wizard"
    _description = "Linked Record Wizard"

    linked_record_ref = fields.Reference(
        selection="_select_target_model",
        string="Linked Record",
    )

    @api.model
    def _select_target_model(self):
        if self.env.context.get("default_linked_model"):
            model_name = self.env.context.get("default_linked_model")
            model = self.env["ir.model"]._get(model_name)
            return [(model_name, model.name)]
        else:
            return []

    def action_save_linked_record(self):
        """
        Action to save the linked record
        """
        if self.env.context.get("create_attribute_value"):
            product_attribute = self.env["product.attribute"].browse(
                self._context.get("active_id")
            )
            record_ref = self.linked_record_ref
            self.env["product.attribute.value"].create(
                [
                    {
                        "linked_record_ref": f"{record_ref._name},{record_ref.id}",
                        "name": record_ref[product_attribute.linked_field_id.name],
                        "attribute_id": product_attribute.id,
                    }
                ]
            )
        else:
            product_attribute_value = self.env["product.attribute.value"].browse(
                self._context.get("active_id")
            )
            product_attribute_value.write(
                {
                    "linked_record_ref": self.linked_record_ref,
                    "name": self.linked_record_ref[
                        product_attribute_value.attribute_id.linked_field_id.name
                    ],
                }
            )
