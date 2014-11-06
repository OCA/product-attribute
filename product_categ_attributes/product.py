from openerp.osv.orm import Model
from openerp.osv import fields


class ProductCategory(Model):
    _inherit = "product.category"
    _columns = {
        'attribute_group_ids': fields.many2many('attribute.group',
                                                'categ_attr_grp_rel',
                                                'categ_id', 'grp_id',
                                                'Attribute Groups'),
    }


class ProductTroduct(Model):
    _inherit = "product.template"

    def _attr_grp_ids(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            grp_ids = [grp.id for grp in product.categ_id.attribute_group_ids]
            for categ in product.categ_ids:
                grp_ids += [grp.id for grp in categ.attribute_group_ids]
            res[product.id] = list(set(grp_ids))
        return res

    _columns = {
        'attribute_group_ids': fields.function(_attr_grp_ids, type='many2many',
                                               relation='attribute.group',
                                               string='Groups')
    }
