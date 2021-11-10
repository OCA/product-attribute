# Copyright 2017 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class ProductSupplierInfoDuplicateWizard(models.TransientModel):
    _name = "product.supplierinfo.duplicate.wizard"
    _description = "Product Supplier Duplicate Wizard"

    date_start = fields.Date(required=True)
    date_end = fields.Date()
    variation_percent = fields.Float(
        digits="Product Price",
        string="Variation %",
    )

    def action_apply(self):
        Supplierinfo = self.env["product.supplierinfo"]
        new_ids = list()
        for item in Supplierinfo.browse(self.env.context.get("active_ids")):
            new_ids.append(
                item.copy(
                    {
                        "date_start": self.date_start,
                        "date_end": self.date_end,
                        "previous_info_id": item.id,
                        "price": item.price * (1.0 + self.variation_percent / 100.0),
                    }
                ).id
            )
            item.date_end = fields.Date.from_string(self.date_start) - relativedelta(
                days=1
            )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_supplierinfo_type_action"
        )
        if len(new_ids) > 0:
            action["domain"] = [("id", "in", new_ids)]
        else:  # pragma: no cover
            action = {"type": "ir.actions.act_window_close"}
        return action
