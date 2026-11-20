# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _add_missing_fields(self, node, name_manager):
        # Odoo 19 injects hidden <field> nodes for expressions that reference
        # fields not present in the view. When the users allowed to see that
        # expression are not a subset of the users allowed to read the field,
        # Odoo leaves the node without a __groups_key__, making it visible to
        # everyone. Tag it with the field's own access groups so that
        # _postprocess_access_rights removes it for users without permission.
        missing_fields = super()._add_missing_fields(node, name_manager)
        for field_name, (missing_groups, _reasons) in missing_fields.items():
            if missing_groups is not False:
                # Core already set a __groups_key__ for this node.
                continue
            field_groups = name_manager._get_field_groups(field_name)
            if field_groups.is_empty() or field_groups.is_universal():
                continue
            for child in node.iter("field"):
                if child.get("name") != field_name or not child.get("invisible"):
                    continue
                if child.get("__groups_key__"):
                    continue
                child.set("__groups_key__", field_groups.key)
                break
        return missing_fields
