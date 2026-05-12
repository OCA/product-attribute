# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from itertools import groupby

from odoo import _, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _before_reset_default_state_hook(self):
        res = super()._before_reset_default_state_hook()

        cron = self.env.ref(
            "product_state_shortage.ir_cron_reset_product_shortage_state",
            raise_if_not_found=False,
        )
        if not cron or not cron.run_as_queue_job:
            return res

        # This search seems a bit sub-optimal since the Job record is already
        # somewhere inside the stack but the context here does not contain the
        # Job's uuid because it got overridden
        current_job = (
            self.env["queue.job"]
            .sudo()
            .search(
                [
                    ("model_name", "=", "ir.cron"),
                    ("state", "=", "started"),
                    ("name", "=", cron.name),
                ],
                limit=1,
                order="date_started desc",
            )
        )
        if not current_job:
            return res

        templates_by_state = {}
        for state, tmpl_group in groupby(self, key=lambda t: t.product_state_id):
            templates_by_state[state] = list(tmpl_group)

        for state, templates in templates_by_state.items():
            product_list_html = "".join(
                [f"<li>{t._get_html_link()} (ID: {t.id})</li>" for t in templates]
            )

            message = _(
                "<p>The following products were in state <strong>%(current_state)s</strong> "
                "and have been reset to default state <strong>%(default_state)s</strong>:</p>"
                "<ul>%(product_list)s</ul>",
                current_state=state.display_name or _("N/A"),
                default_state=self._get_default_product_state().display_name,
                product_list=product_list_html,
            )
            current_job.message_post(body=message)

        return res
