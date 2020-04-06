# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.osv.orm import setup_modifiers
from lxml import etree

SPECIAL_FIELDS = {"id,", "display_name", "__last_update", "product_id"}


class ProductRelatedFilterMixin(models.AbstractModel):
    _name = "product.related.filter.mixin"
    _description = "Adds seller_id field related with product_id to filter"

    # This declaration in abstract model is needed to declare related field
    product_id = fields.Many2one(comodel_name='product.product')

    @api.model
    def add_filter_related_fields(self, res):
        eview = etree.fromstring(res['arch'])
        # Get defined fields in abstract model, but discard special fields or
        # already defined in the view
        fields_dic = {}
        for k, v in self.env["product.related.filter.mixin"]._fields.items():
            if k in SPECIAL_FIELDS or (
                    eview.xpath("//field[@name={}]".format(k))):
                continue
            fields_dic[k] = v
        for k_field, v_field in fields_dic.items():
            res['fields'].update({
                k_field: {
                    'type': v_field.type,
                    'string': _(v_field.string),
                }
            })
        for node in (eview.xpath("//field[@name='product_id']") or
                     eview.xpath("//field[@name='categ_id']") or
                     eview.xpath("//field[last()]")):
            # Add fields in search view
            for k_field, v_field in fields_dic.items():
                elem = etree.Element(
                    'field',
                    {
                        'name': k_field,
                        'string': _(v_field.string),
                    })
                setup_modifiers(elem)
                node.addnext(elem)
                res['arch'] = etree.tostring(eview)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """ Inject fields field in search views. """
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu
        )
        if view_type != 'search':  # pragma: no cover
            return res
        return self.add_filter_related_fields(res)
