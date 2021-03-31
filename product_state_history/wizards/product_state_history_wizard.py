# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductStateHistoryWizard(models.TransientModel):

    _name = 'product.state.history.wizard'
    _description = 'Product State History Report'

    pivot_date = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
    )
    product_state = fields.Selection(
        selection=[
            ('draft', 'In Development'),
            ('sellable', 'Normal'),
            ('end', 'End of Lifecycle'),
            ('obsolete', 'Obsolete')
        ],
        string='Product Status',
        required=True,
    )

    @api.multi
    def _get_product_domain(self):
        # Get product history for the actual product state
        self.ensure_one()
        return [
            ('state_date', '>=', self.pivot_date),
            ('product_state', '=', self.product_state),
            ('product_template_id.state', '=', self.product_state),
            ('product_template_id.active', '=', True),
        ]

    @api.multi
    def print_report(self):
        for wizard in self:
            history_obj = self.env['product.state.history']
            products = list()
            histories = self.env['product.state.history'].search(
                wizard._get_product_domain())
            # As product state history is ordered by id desc, we take
            # the first one by product
            history_report = history_obj.browse()
            for history in histories:
                product = history.product_template_id
                if product not in products:
                    products.append(product)
                    history_report |= history

            datas = {
                'ids': history_report.ids,
                'model': 'product.state.history',
                'form': {'pivot_date': wizard.pivot_date}
            }

            return self.env['report'].with_context(landscape=True).get_action(
                history_report.ids,
                'product_state_history.report_product_state_history',
                data=datas)
