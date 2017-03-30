# -*- coding: utf-8 -*-
# (c) 2017 Consultoría Informática Studio73 SL (contacto@studio73.es)
#          Pablo Fuentes <pablo@studio73.es>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ProductFamily(models.Model):
    _name = 'product.family'
    _parent_name = "parent_id"
    _order = 'parent_left'
    _parent_order = "sequence asc, name"
    _parent_store = True

    sequence = fields.Integer(string="Sequence")
    name = fields.Char('Nombre', required=True, translate=True)
    parent_id = fields.Many2one(comodel_name="product.family", string="Parent Family", ondelete='cascade')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)
    type = fields.Selection(selection=[('view', 'View'), ('normal', 'Normal')],
                            string="Family Type", default="normal")

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive Families.'))
        return True

    @api.multi
    def name_get(self):
        def get_names(family):
            res = []
            while family:
                res.append(family.name)
                family = family.parent_id
            return res

        return [(family.id, " / ".join(reversed(get_names(family)))) for family in self]

    @api.multi
    def write(self, values):
        res = super(ProductFamily, self).write(values)
        if 'sequence' in values:
            self._parent_store_compute()
        return res
