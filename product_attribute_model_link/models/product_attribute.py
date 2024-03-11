# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval

_logger = logging.getLogger(__name__)


def make_create():
    """Instantiate a create method that generates new product attribute values
    based on the current record."""

    @api.model_create_multi
    def create(self, vals_list, **kw):
        product_attributes = self.env["product.attribute"].search(
            [("linked_model_id", "=", self._name)]
        )
        # Call original method
        records = create.origin(self, vals_list, **kw)
        if not product_attributes or self.env.context.get(
            "operation_from_attribute_value"
        ):
            return records

        for product_attribute in product_attributes:
            matching_domain_records = product_attribute._filter_domain(records)
            for record in matching_domain_records:
                related_record = record[product_attribute.linked_field_id.name]
                # Attempt conversion for digital field
                try:
                    name_value = str(related_record) if related_record else ""
                except Exception as e:
                    # Handle exception if conversion fails
                    raise ValidationError(
                        _(
                            "Conversion failed for field 'name' on creation of "
                            "product.attribute.value. Please check the data."
                        )
                    ) from e
                self.env["product.attribute.value"].with_context(
                    operation_from_record=True
                ).create(
                    {
                        "name": name_value,
                        "linked_record_ref": f"{record._name},{record.id}",
                        "attribute_id": product_attribute.id,
                    }
                )
        return records

    return create


def make_write():
    """Instantiate a write method that modifies linked product attribute values
    based on the current record."""

    def write(self, vals, **kw):
        # Retrieve connected product attribute values for all records in the set
        product_attribute_values = self.env["product.attribute.value"].search(
            [("linked_record_ref", "in", [f"{rec._name},{rec.id}" for rec in self])]
        )
        # Call original method
        write.origin(self, vals, **kw)

        if not (product_attribute_values and self) or self.env.context.get(
            "operation_from_attribute_value"
        ):
            return True

        # Modify linked product attribute value for each record in the set
        for product_attribute_value in product_attribute_values:
            record = product_attribute_value.linked_record_ref
            linked_field_name = (
                product_attribute_value.attribute_id.linked_field_id.name
            )
            # Check if linked field is in vals before updating
            if linked_field_name in vals:
                product_attribute_value.with_context(operation_from_record=True).write(
                    {"name": record[linked_field_name]}
                )
        return True

    return write


def make_unlink():
    """Instantiate an unlink method that unlinks linked product attribute values
    or deactivates them if they are associated with a product."""

    def unlink(self, **kwargs):
        if not self.env.context.get("operation_from_attribute_value"):
            # Retrieve connected product attribute values for all records in the set
            product_attribute_values = self.env["product.attribute.value"].search(
                [("linked_record_ref", "in", [f"{rec._name},{rec.id}" for rec in self])]
            )
            for product_attribute_value in product_attribute_values:
                linked_products = (
                    self.env["product.template.attribute.value"]
                    .search(
                        [
                            (
                                "product_attribute_value_id",
                                "=",
                                product_attribute_value.id,
                            )
                        ]
                    )
                    .with_context(active_test=False)
                )
                # Archive or unlink the product attribute value based on linked products
                if linked_products:
                    product_attribute_value.with_context(
                        operation_from_record=True
                    ).write({"active": False})
                else:
                    product_attribute_value.with_context(
                        operation_from_record=True
                    ).unlink()
        # Call original method
        return unlink.origin(self, **kwargs)

    return unlink


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    linked_model_id = fields.Many2one(
        "ir.model",
        "Linked model",
        domain="[('transient', '=', False)]",
        help="Model which records will be used for the attribute values. "
        "Cannot be a transient model. Warning: changing or removing "
        "existing value will not affect existing attribute values!",
    )
    res_model_name = fields.Char(string="Model", related="linked_model_id.model")
    linked_field_id = fields.Many2one(
        "ir.model.fields",
        "Linked field",
        domain="[('store', '=', True), ('relation', '=', False), "
        "('model_id', '=', linked_model_id)]",
        help="Field of the selected model that will be used for the attribute value names. "
        "Can be any field except for related or computed non-stored ones. "
        "Digital field values will be converted to Char automatically. "
        "Warning: changing or removing existing value will "
        "not affect existing attribute values!",
    )
    domain = fields.Char(
        string="Domain (optional)",
        help="If configured only records matching the domain will be used "
        "for attribute value creation. "
        "Warning: updating domain will not affect existing attribute values!",
        default="[]",
    )
    apply_to_products_on_create = fields.Boolean(
        help="If enabled when a new attribute value is created "
        "it will be automatically added "
        "to all existing products that use this attribute. Attention! "
        "You must completely understand possible consequences and use this option with care!"
    )
    create_from_attribute_values = fields.Boolean(
        help="If enabled when a new attribute value is added to the attribute "
        "a new record will be created in the linked model. Attention! "
        "The only value passed explicitly on creation will be the linked field "
        "containing the new attribute value name. "
        "You must ensure that this would be enough for new record creation. "
        "Otherwise an exception will be raised. "
        "If a digital field is used a conversion attempt will be done. "
        "If conversion fails an exception might be raised."
    )
    modify_from_attribute_values = fields.Boolean(
        help="If enabled when an attribute value is renamed linked field "
        "value in the linked model will be updated accordingly. "
        "If a digital field is used a conversion attempt will be done. "
        "If conversion fails an exception might be raised. "
        "This option is available only if 'Create from Attribute Values' option is enabled."
    )
    delete_when_attribute_value_is_deleted = fields.Boolean(
        help="When enabled if an attribute value is deleted linked "
        "record will be deleted too. "
        "Use with extreme care! This option is available only "
        "if 'Create from Attribute Values' option is enabled."
    )

    @api.onchange("domain")
    def _onchange_domain(self):
        if self.domain:
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _(
                        "Updating domain will not affect existing attribute values!"
                    ),
                },
            }

    @api.onchange("apply_to_products_on_create")
    def _onchange_apply_to_products_on_create(self):
        if self.apply_to_products_on_create:
            return {
                "warning": {
                    "title": _("Attention!"),
                    "message": _(
                        "You must completely understand possible "
                        "consequences and use this option with care!"
                    ),
                },
            }

    @api.onchange("create_from_attribute_values")
    def _onchange_create_from_attribute_values(self):
        if self.create_from_attribute_values:
            return {
                "warning": {
                    "title": _("Attention!"),
                    "message": _(
                        "The only value passed explicitly on creation will be the linked field "
                        "containing the new attribute value name. "
                    ),
                },
            }

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            if vals.get("linked_field_id"):
                self._update_registry()
        return res

    def write(self, vals):
        res = super().write(vals)
        if vals.get("linked_field_id"):
            self._update_registry()
        return res

    def unlink(self):
        res = super().unlink()
        self._update_registry()
        return res

    def _update_registry(self):
        """Update the registry by unregistering and then registering the hook."""
        self._unregister_hook()
        self._register_hook()

    def _get_eval_context(self):
        """Prepare the context used when evaluating python code
        :returns: dict -- evaluation context given to safe_eval
        """
        return {
            "datetime": safe_eval.datetime,
            "dateutil": safe_eval.dateutil,
            "time": safe_eval.time,
            "uid": self.env.uid,
            "user": self.env.user,
        }

    def _filter_domain(self, records):
        """
        Filters records based on a defined domain, preserving original order.

        :param records: Recordset to be filtered.
        :return: Filtered recordset based on the defined domain
        while maintaining the original order.
        """
        self_sudo = self.sudo()
        if self_sudo.domain and records:
            domain = safe_eval.safe_eval(self_sudo.domain, self._get_eval_context())
            return records.sudo().filtered_domain(domain).with_env(records.env)
        else:
            return records

    def _register_hook(self):
        """Patch models that should trigger action rules based on creation,
        modification or deletion of records.
        """

        patched_models = defaultdict(set)

        def patch(model, name, method):
            """Patch method `name` on `model`, unless it has been patched already."""
            if model not in patched_models[name]:
                patched_models[name].add(model)
                ModelClass = type(model)
                origin = getattr(ModelClass, name)
                method.origin = origin
                wrapped = api.propagate(origin, method)
                wrapped.origin = origin
                setattr(ModelClass, name, wrapped)

        # Retrieve all product attributes, and patch their corresponding model
        product_attributes = self.search(
            [("linked_model_id", "!=", False), ("linked_field_id", "!=", False)]
        )
        for product_attribute in product_attributes:
            Model = self.env.get(product_attribute.linked_model_id.model)
            patch(Model, "create", make_create())
            patch(Model, "write", make_write())
            patch(Model, "unlink", make_unlink())

    def _unregister_hook(self):
        """Remove the patches installed by _register_hook()"""
        NAMES = ["create", "write", "unlink"]
        patched_models = []

        # Retrieve the models that were patched during _register_hook
        for product_attribute in self.search(
            [("linked_model_id", "!=", False), ("linked_field_id", "!=", False)]
        ):
            patched_models.append(product_attribute.linked_model_id.model)

        for model in patched_models:
            Model = self.env.registry[model]
            # Remove patched attributes from the previously patched models
            for name in NAMES:
                try:
                    delattr(Model, name)
                except AttributeError as e:
                    _logger.warning(
                        "AttributeError occurred while removing patch: %s", e
                    )

    def add_attribute_value_from_linked_record(self):
        """
        Action to open a wizard for the linked record.

        :return: Action dictionary to open the wizard.
        """
        context = {
            "default_linked_model": self.linked_model_id.model
            if self.linked_model_id
            else False,
            "create_attribute_value": True,
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
