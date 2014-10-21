# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class IrModelFields(Model):

    _inherit = "ir.model.fields"
    _columns = {'field_description': fields.char('Field Label', required=True,
                                                 size=256, translate=True)}
    _sql_constraints = [('name_model_uniq', 'unique (name, model_id)',
                         """The name of the field has to be
 uniq for a given model !""")]
