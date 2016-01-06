# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


KEEP_FIELD_HELP = "Whatever '%s' field, if checked then old value is kept"


class ProductPriceitemTransient(models.TransientModel):
    _name = 'product.priceitem.transient'
    _description = "Wizard Price Items"

    def _get_products_info(self):
        context = self.env.context.copy()
        product_ids = context.get('active_ids', [])
        elm = []
        for prd in self.env['product.template'].search([
                ('id', 'in', product_ids)]):
            info = prd.name
            if prd.default_code:
                info = '%s, %s' % (prd.default_code, prd.name)
            elm.append(info)
        return '\n'.join(elm)

    @api.multi
    def apply(self):
        context = self.env.context.copy()
        active_ids = context.get('active_ids')
        if not active_ids:
            raise UserError(_("No product ids"))
        # TODO FIX: context['price_version_id'] is not propagated until here
        # extracted the value from active_domain below
        price_version_id = context.get('active_domain', False)
        if not price_version_id:
            raise UserError(_("No version %s" % context))
        mode = 'apply_existing_items'
        if price_version_id[0] == '|':
            mode = 'apply_new_items'
        if mode == 'apply_new_items':
            price_version_id = price_version_id[2][2]
        else:
            price_version_id = price_version_id[0][2]
        vals = {}
        for elm in self:
            if elm.keep_price and elm.keep_sequence:
                raise UserError(
                    _("'Keep Price' and 'Keep Sequence' checkboxes "
                      "are checked.\n"
                      "Remove one of these for that action can be done"))
            if not elm.keep_price:
                vals['price_surcharge'] = elm.price
            if not elm.keep_sequence:
                vals['sequence'] = elm.sequence
        price_items = self.env['product.pricelist.item'].search(
            [('price_version_id', '=', price_version_id),
             ('product_tmpl_id', 'in', active_ids)])
        if vals:
            if mode == 'apply_existing_items':
                price_items.write(vals)
            else:
                price_items.create(vals)
        return {
            'res_model': 'product.pricelist.version',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'view_mode': 'form,tree',
            'res_id': price_version_id,
        }

    price = fields.Float()
    sequence = fields.Integer(default=1)
    keep_price = fields.Boolean(
        string="Keep Existing Price",
        default=True,
        help=KEEP_FIELD_HELP % 'Price')
    keep_sequence = fields.Boolean(
        string="Keep Existing Sequence",
        default=True,
        help=KEEP_FIELD_HELP % 'Sequence')
    products = fields.Text(
        string="Impacted Products",
        default=_get_products_info,
        readonly=True)
