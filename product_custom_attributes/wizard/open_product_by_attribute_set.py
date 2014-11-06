# -*- coding: utf-8 -*-
from openerp.osv.orm import TransientModel
from openerp.osv import fields


class OpenProductByAttributeSet(TransientModel):
    _name = 'open.product.by.attribute.set'
    _description = 'Wizard to open product by attributes set'

    _columns = {
        'attribute_set_id': fields.many2one('attribute.set', 'Attribute Set'),
    }

    def open_product_by_attribute(self, cr, uid, ids, context=None):
        """
        Opens Product by attributes
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of account chart’s IDs
        @return: dictionary of Product list window for a given attributes set
        """
        mod_obj = self.pool['ir.model.data']
        act_obj = self.pool['ir.actions.act_window']
        att_group_obj = self.pool['attribute.group']
        if context is None:
            context = {}
        attribute_set = self.browse(cr, uid, ids[0],
                                    context=context).attribute_set_id
        result = mod_obj.get_object_reference(cr, uid, 'product',
                                              'product_template_action')
        id = result[1] if result else False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        grp_ids = att_group_obj.search(cr, uid, [('attribute_set_id', '=',
                                                  attribute_set.id)],
                                       context=context)
        ctx = "{'open_product_by_attribute_set': %s, \
              'attribute_group_ids': %s}" % (True, grp_ids)
        result['context'] = ctx
        result['domain'] = "[('attribute_set_id', '=', %s)]" % attribute_set.id
        result['name'] = attribute_set.name
        return result
