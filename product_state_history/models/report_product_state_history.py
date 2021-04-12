# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ReportProductStateHistory(models.AbstractModel):

    _name = "report.product_state_history.report_product_state_history"

    @api.model
    def render_html(self, docids, data=None):
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
        return self.env["report"].render(
            "product_state_history.report_product_state_history", docargs
        )
