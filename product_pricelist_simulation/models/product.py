# -*- coding: utf-8 -*-
# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _render_block(self, columns, pricelist, price):
        render = """
        <div class="col-md-%s">
            <div class="col-md-12"><strong>%s</strong></div>
            <div class="col-md-12">%s %s</div>
        </div>
        """ % (columns, pricelist.name, pricelist.currency_id.symbol, price)
        return render

    @api.multi
    def _compute_pricelist_simulate(self):
        self.ensure_one()
        pricelists = self.env['product.pricelist'].search([])
        precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        pricelist_blocks = ""
        columns = 12 / len(pricelists)
        for pricelist in pricelists:
            price = round(
                self.with_context(pricelist=pricelist.id).price, precision)
            pricelist_blocks += self._render_block(columns, pricelist, price)
        self.pricelist_simulate = "<div class='row'>%s</div>" % (
            pricelist_blocks)

    pricelist_simulate = fields.Html(
        compute=_compute_pricelist_simulate,
        string='Pricelist Simulate',
    )
