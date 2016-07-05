# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp.osv.osv import except_osv
from openerp.tools.translate import _


from openerp import models, fields
from openerp import api


class ProductCategory(models.Model):
    _inherit = "product.category"
    
    attribute_group_ids = fields.Many2many(comodel_name="attribute.group",
                                            relation="categ_attr_grp_rel", column1="categ_id", column2="grp_id", string="Attribute Group")
    
    

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.v7
    def _attr_grp_ids(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            grp_ids = [grp.id for grp in product.categ_id.attribute_group_ids]
            for categ in product.categ_ids:
                grp_ids += [grp.id for grp in categ.attribute_group_ids]
            res[product.id] = list(set(grp_ids))
        return res

