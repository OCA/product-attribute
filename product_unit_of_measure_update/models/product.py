# coding: utf-8
# © 2016 David BEAL @ Akretion <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        uom_values = {
            'uom_id': vals.get('uom_id'),
            'uom_po_id': vals.get('uom_po_id'),
        }
        clauses = []
        vals_copy = vals.copy()
        for key, uom_value in uom_values.items():
            if uom_value:
                clauses.append("%s = %s" % (key, uom_value))
                vals_copy.pop(key)
        if clauses and not self._products_used_in_db():
            params = {'ids': '(%s)' % ', '.join([str(x) for x in self._ids]),
                      'upd': ', '.join(clauses)}
            query = "UPDATE product_template SET %(upd)s WHERE id in %(ids)s"
            self._cr.execute(query % params)
        return super(ProductTemplate, self).write(vals_copy)

    @api.multi
    def _products_used_in_db(self):
        used_products = False
        for product in self:
            # Optimization could be done here by searching first tables
            # where there is a higher probability to contains products data
            # recently created like:
            # stock.move, mrp.bom.line, sale.order.line
            # NotImplementForNow
            erp_fields = self.env['ir.model.fields'].search([
                ('relation', '=', 'product.product'),
                ('model_id.model', 'not in',
                    self._exclude_models_with_product_foreign_key()),
                ('ttype', '=', 'many2one')])
            for field in erp_fields:
                res = self.env[field.model_id.model].search([
                    (field.name, 'in', product.product_variant_ids.ids)])
                used_products = used_products or len(res)
                if used_products:
                    return True
        return used_products

    @api.model
    def _exclude_models_with_product_foreign_key(self):
        """ List of models on which no check are required
            because another model with m2o is defined on it
            You can customized this list according to
            your instance dependencies.
        """
        return [
            'report.stock.lines.date',  # dependency on stock.move first
        ]
