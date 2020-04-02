# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.fr/>)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: La Louve
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html

from odoo import models, api


class ConfirmUpdateWizard(models.TransientModel):
    _name = 'confirm.update.wizard'
    _description = 'Confirm Update Wizard'

    @api.multi
    def confirm_update(self):
        self.ensure_one()
        products_to_send = self.env['product.product'].search([
            ('scale_group_id', '!=', False)])
        products_to_send.send_scale_write()
        return True
