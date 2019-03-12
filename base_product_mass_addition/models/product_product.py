# © 2014 Today Akretion
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models
from odoo.tests.common import Form


class ProductProduct(models.Model):
    _inherit = 'product.product'

    qty_to_process = fields.Float(
        compute='_compute_process_qty',
        inverse='_inverse_set_process_qty',
        help="Set this quantity to create a new line "
             "for this product or update the existing one."
    )

    def _prepare_quick_line(self, parent):
        res = self._get_quick_line_qty_vals()
        res.update({'product_id': self.id})
        return res

    def _get_quick_line(self, parent):
        raise NotImplementedError

    def _add_quick_line(self, parent, line_model):
        vals = self._prepare_quick_line(parent)
        vals = self._complete_quick_line_vals(False, vals)
        if not vals.get('price_unit'):
            vals['price_unit'] = 0.0
        self.env[line_model].create(vals)

    def _update_quick_line(self, line):
        if self.qty_to_process:
            # apply the on change to update price unit if depends on qty
            vals = self._get_quick_line_qty_vals()
            vals = self._complete_quick_line_vals(line, vals)
            line.write(vals)
        else:
            line.unlink()

    def _get_quick_line_qty_vals(self):
        raise NotImplementedError

    def _complete_quick_line_vals(self, line, vals, view=False, parent_key=''):
        if not view:
            raise NotImplementedError
        form_line = None
        if line:
            form_line = Form(line, view=view['ref'])
        else:
            form_line = Form(self.env[view['model']], view=view['ref'])
        init_keys = ['product_id', parent_key]
        init_vals = [(key, val) for key, val in vals.items()
                     if key in init_keys]
        form_line._values.update(init_vals)
        form_line._perform_onchange(init_keys)
        update_keys = [key for key in vals.keys() if key not in init_keys]
        update_vals = [(key, val) for key, val in vals.items()
                       if key not in init_keys]
        form_line._values.update(update_vals)
        form_line._perform_onchange(update_keys)
        return form_line._values

    def _inverse_set_process_qty(self):
        parent_model = self.env.context.get('parent_model')
        parent_id = self.env.context.get('parent_id')
        if parent_model:
            parent = self.env[parent_model].browse(parent_id)
            for product in self:
                quick_line = self._get_quick_line(parent)
                if quick_line:
                    product._update_quick_line(quick_line)
                else:
                    product._add_quick_line(parent, quick_line._name)

    def _compute_process_qty(self):
        if not self.env.context.get('parent_id'):
            return

    @api.multi
    def button_return_parent(self):
        self.ensure_one()
        parent_id = self.env.context.get('parent_id')
        parent_model = self.env.context.get('parent_model')
        if parent_id:
            parent = self.env[parent_model].browse(parent_id)
            return {
                'name': parent.display_name,
                'type': 'ir.actions.act_window',
                'res_model': parent_model,
                'view_mode': 'form',
                'res_id': parent_id,
            }
