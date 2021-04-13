# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductStateHistoryWizard(models.TransientModel):

    _name = "product.state.history.wizard"
    _description = "Product State History Report"

    pivot_date = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
    )
    product_state_id = fields.Many2one(
        comodel_name="product.state",
        string="Product Status",
        required=True,
    )

    def _get_product_domain(self):
        # Get product history for the actual product state
        self.ensure_one()
        return [
            ("state_date", ">=", self.pivot_date),
            ("product_state_id", "=", self.product_state_id.id),
            ("product_template_id.product_state_id", "=", self.product_state_id.id),
            ("product_template_id.active", "=", True),
        ]

    def print_report(self):
        for wizard in self:
            history_obj = self.env["product.state.history"]
            products = list()
            histories = self.env["product.state.history"].search(
                wizard._get_product_domain()
            )
            # As product state history is ordered by id desc, we take
            # the first one by product
            history_report = history_obj.browse()
            for history in histories:
                product = history.product_template_id
                if product not in products:
                    products.append(product)
                    history_report |= history

            datas = {
                "ids": history_report.ids,
                "model": "product.state.history",
                "form": {"pivot_date": wizard.pivot_date},
            }
            return (
                self.env.ref(
                    "product_state_history.action_report_product_state_history"
                )
                .with_context(landscape=True)
                .report_action(
                    history_report.ids,
                    data=datas,
                )
            )
