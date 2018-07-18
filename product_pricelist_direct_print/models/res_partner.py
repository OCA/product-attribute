# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def action_customer_pricelist_email_send(self):
        wiz = self.env['product.pricelist.print']
        for partner in self.filtered(lambda x: not x.parent_id):
            wiz.create({
                'partner_id': partner.id,
                'pricelist_id': partner.property_product_pricelist.id,
            }).force_pricelist_send()
