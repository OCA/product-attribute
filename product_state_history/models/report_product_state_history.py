# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ReportProductStateHistory(models.AbstractModel):

    _name = "report.product_state_history.report_product_state_history"
    _description = "Product State History Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data if data is not None else {}
        history_ids = self.env["product.state.history"].browse(data.get("ids", docids))
        docargs = {
            "doc_ids": data.get("ids", data.get("active_ids")),
            "doc_model": "product.state.history",
            "docs": history_ids,
            "data": dict(
                data,
            ),
        }
        return docargs
