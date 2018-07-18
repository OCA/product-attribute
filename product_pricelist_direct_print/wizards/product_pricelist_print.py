# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelistPrint(models.TransientModel):
    _name = 'product.pricelist.print'

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )
    categ_ids = fields.Many2many(
        comodel_name='product.category',
        string='Categories',
    )
    show_variants = fields.Boolean()
    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        string='Products',
        help='Keep empty for all products',
    )
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Products',
        help='Keep empty for all products',
    )
    show_standard_price = fields.Boolean(string='Show Cost Price')
    show_sale_price = fields.Boolean(string='Show Sale Price')
    order_field = fields.Selection([
        ('name', 'Name'),
        ('default_code', 'Internal Reference'),
    ], string='Order')

    @api.model
    def default_get(self, fields):
        res = super(ProductPricelistPrint, self).default_get(fields)
        if self.env.context.get('active_model') == 'product.template':
            res['product_tmpl_ids'] = [
                (6, 0, self.env.context.get('active_ids', []))]
        elif self.env.context.get('active_model') == 'product.product':
            res['show_variants'] = True
            res['product_ids'] = [
                (6, 0, self.env.context.get('active_ids', []))]
        elif self.env.context.get('active_model') == 'product.pricelist':
            res['pricelist_id'] = self.env.context.get('active_id', False)
        elif self.env.context.get('active_model') == 'res.partner':
            res['partner_id'] = self.env.context.get('active_id', False)
            partner = self.env['res.partner'].browse(
                self.env.context.get('active_id', False))
            res['pricelist_id'] = partner.property_product_pricelist.id
        return res

    @api.multi
    def print_report(self):
        if not(self.pricelist_id or self.show_standard_price or
               self.show_sale_price):
            raise ValidationError(_(
                'You must set price list or any show price option.'))
        return self.env.ref(
            'product_pricelist_direct_print.'
            'action_report_product_pricelist').report_action(self)

    @api.multi
    def action_pricelist_send(self):
        self.ensure_one()
        template_id = self.env.ref(
            'product_pricelist_direct_print.email_template_edi_pricelist').id
        compose_form_id = self.env.ref(
            'mail.email_compose_message_wizard_form').id
        ctx = {
            'default_composition_mode': 'comment',
            'default_res_id': self.id,
            'default_model': 'product.pricelist.print',
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'partner_to': self.partner_id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def force_pricelist_send(self):
        if self.env.context.get('active_model') != 'res.partner':
            return False
        template_id = self.env.ref(
            'product_pricelist_direct_print.email_template_edi_pricelist').id
        composer = self.env['mail.compose.message'].with_context({
            'default_composition_mode': 'mass_mail',
            'default_notify': True,
            'default_res_id': self.id,
            'default_model': 'product.pricelist.print',
            'default_template_id': template_id,
            'active_ids': self.ids,
            'partner_to': self.partner_id,
        }).create({})
        values = composer.onchange_template_id(
            template_id, 'mass_mail', 'product.pricelist.print',
            self.id)['value']
        composer.write(values)
        composer.send_mail()
