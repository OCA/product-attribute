# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   base_attribute.attributes for OpenERP                                     #
#   Copyright (C) 2011 Akretion Benoît GUILLOT <benoit.guillot@akretion.com>
#   Copyright (C) 2013 Akretion Raphaël VALYI <raphael.valyi@akretion.com>
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import ast
from openerp import models, fields, api
from openerp.osv import orm
from openerp.tools.translate import _
from lxml import etree
from unidecode import unidecode  # Debian package python-unidecode
import re


def safe_column_name(string):
    """This function prevent portability problem in database column name
    with other DBMS system
    Use case : if you synchronise attributes with other applications """
    string = unidecode(string.replace(' ', '_').lower())
    return re.sub(r'[^0-9a-z_]', '', string)


class AttributeOption(models.Model):
    _name = "attribute.option"
    _description = "Attribute Option"
    _order = "sequence"

    @api.model
    def _get_model_list(self):
        model_pool = self.env['ir.model']
        models = model_pool.search([])
        return [(model.model, model.name) for model in models]

    name = fields.Char(
        size=128,
        translate=True,
        required=True)
    value_ref = fields.Reference(
        string='Reference',
        selection='_get_model_list',
        size=128)
    attribute_id = fields.Many2one(
        comodel_name='attribute.attribute',
        string='Product Attribute',
        required=True)
    sequence = fields.Integer()

    @api.onchange('name')
    def name_change(self):
        if self.attribute_id.relation_model_id:
            warning = {'title': _('Error!'),
                       'message': _("Use the 'Load Options' button "
                                    "instead to select appropriate "
                                    "model references'")}
            return {"value": {"name": False}, "warning": warning}


class AttributeOptionWizard(models.TransientModel):
    _name = "attribute.option.wizard"
    _rec_name = 'attribute_id'

    attribute_id = fields.Many2one(
        comodel_name='attribute.attribute',
        string='Product Attribute',
        required=True,
        default=lambda self: self._context.get('active_id', False))

    @api.multi
    def validate(self):
        return True

    @api.model
    def create(self, vals):
        attr_obj = self.env["attribute.attribute"]
        attr = attr_obj.browse(vals['attribute_id'])
        attr.option_ids.unlink()
        opt_obj = self.env["attribute.option"]
        for op_id in (
                vals.get("option_ids") and vals['option_ids'][0][2] or []):
            relation_model = attr.relation_model_id.model
            name = self.env[relation_model].browse(op_id).name_get()[0][1]
            opt_obj.create({
                'attribute_id': vals['attribute_id'],
                'name': name,
                'value_ref': "%s,%s" % (attr.relation_model_id.model, op_id)
            })
        res = super(AttributeOptionWizard, self).create(vals)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(AttributeOptionWizard, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self._context.get("active_id"):
            model_obj = self.env[self._context.get('active_model')].browse(
                self._context.get("active_id")).relation_model_id
            relation = model_obj.model
            res['fields'].update(
                {'option_ids': {
                    'domain': [],
                    'string': "Options",
                    'type': 'many2many',
                    'relation': relation,
                    'required': True}})
            eview = etree.fromstring(res['arch'])
            options = etree.Element('field', name='option_ids', colspan='6')
            placeholder = eview.xpath(
                "//separator[@string='options_placeholder']")[0]
            placeholder.getparent().replace(placeholder, options)
            res['arch'] = etree.tostring(eview, pretty_print=True)
        return res


class AttributeAttribute(models.Model):
    _name = "attribute.attribute"
    _description = "Attribute"

    @api.model
    def _build_attribute_field(self, page, attribute):
        parent = etree.SubElement(page, 'group', colspan="2", col="4")
        kwargs = {'name': "%s" % attribute.name}
        if attribute.ttype in ['many2many', 'text']:
            parent = etree.SubElement(parent, 'group', colspan="2", col="4")
            etree.SubElement(
                parent,
                'separator',
                string="%s" % attribute.field_description,
                colspan="4")
            kwargs['nolabel'] = "1"
        if attribute.ttype in ['many2one', 'many2many']:
            if attribute.relation_model_id:
                # attribute.domain is a string, it may be an empty list
                try:
                    domain = ast.literal_eval(attribute.domain)
                except ValueError:
                    domain = None
                if domain:
                    kwargs['domain'] = attribute.domain
                else:
                    ids = [op.value_ref.id for op in attribute.option_ids]
                    kwargs['domain'] = "[('id', 'in', %s)]" % ids
            else:
                kwargs['domain'] =\
                    "[('attribute_id', '=', %s)]" % attribute.attribute_id.id
        kwargs['context'] =\
            "{'default_attribute_id': %s}" % attribute.attribute_id.id
        kwargs['required'] = str(attribute.required or
                                 attribute.required_on_views)
        field = etree.SubElement(parent, 'field', **kwargs)
        orm.setup_modifiers(field, self.fields_get(attribute.name))
        return parent

    @api.model
    def _build_attributes_notebook(self, attribute_group_ids):
        notebook = etree.Element('notebook', name="attributes_notebook",
                                 colspan="4")
        toupdate_fields = []
        grp_obj = self.env['attribute.group']
        for group in grp_obj.browse(attribute_group_ids):
            page = etree.SubElement(notebook, 'page',
                                    string=group.name.capitalize())
            for attribute in group.attribute_ids:
                if attribute.name not in toupdate_fields:
                    toupdate_fields.append(attribute.name)
                    self._build_attribute_field(page, attribute)
        return notebook, toupdate_fields

    @api.onchange('relation_model_id')
    def relation_model_id_change(self):
        "removed selected options as they would be inconsistent"
        return {'value': {'option_ids': [(2, i[1]) for i in self.option_ids]}}

    @api.multi
    def button_add_options(self):
        self.ensure_one()
        wizard_form = self.env.ref(
            'base_custom_attributes.attribute_option_wizard_form_view', False)
        return {
            'name': _('Options Wizard'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'attribute.option.wizard',
            'type': 'ir.actions.act_window',
            'views': [(wizard_form.id, 'form')],
            'view_id': wizard_form.id,
            'target': 'new',
        }

    @api.model
    def _get_default_model(self):
        context = self._context
        if context and context.get('force_model'):
            default_model = self.env['ir.model'].search(
                [('model', '=', context['force_model'])])
            if default_model:
                return default_model
        return None

    field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Ir Model Fields',
        required=True,
        delegate=True,
        ondelete="cascade")
    attribute_type = fields.Selection(selection=[
        ('char', 'Char'),
        ('text', 'Text'),
        ('select', 'Select'),
        ('multiselect', 'Multiselect'),
        ('boolean', 'Boolean'),
        ('integer', 'Integer'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('binary', 'Binary'),
        ('float', 'Float')],
        string='Type',
        required=True)
    serialized = fields.Boolean(
        string='Field serialized',
        help="If serialized, the field will be stocked in the serialized "
        "field: attribute_custom_tmpl or attribute_custom_variant "
        "depending on the field based_on")
    option_ids = fields.One2many(
        comodel_name='attribute.option',
        inverse_name='attribute_id',
        string='Attribute Options')
    create_date = fields.Datetime(
        string='Created date',
        readonly=True)
    relation_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model')
    required_on_views = fields.Boolean(
        string='Required (on views)',
        help="If activated, the attribute will be mandatory on the views, "
        "but not in the database")

    _defaults = {
        'model_id': _get_default_model
    }

    @api.model
    def create(self, vals):
        """ Create an attribute.attribute

        When a `field_id` is given, the attribute will be linked to the
        existing field. The use case is to create an attribute on a field
        created with Python `fields`.

        """
        if vals.get('field_id'):
            # when a 'field_id' is given, we create an attribute on an
            # existing 'ir.model.fields'.  As this model `_inherits`
            # 'ir.model.fields', calling `create()` with a `field_id`
            # will call `write` in `ir.model.fields`.
            # When the existing field is not a 'manual' field, we are
            # not allowed to write on it. So we call `create()` without
            # changing the fields values.
            field_obj = self.env['ir.model.fields']
            field = field_obj.browse(vals['field_id'])
            if vals.get('serialized'):
                raise orm.except_orm(
                    _('Error'),
                    _("Can't create a serialized attribute on "
                      "an existing ir.model.fields (%s)") % field.name)
            if field.state != 'manual':
                # the ir.model.fields already exists and we want to map
                # an attribute on it. We can't change the field so we
                # won't add the ttype, relation and so on.
                return super(AttributeAttribute, self).create(vals)

        if vals.get('relation_model_id'):
            relation = self.env['ir.model'].browse(
                vals.get('relation_model_id')).model
        else:
            relation = 'attribute.option'
        if vals['attribute_type'] == 'select':
            vals['ttype'] = 'many2one'
            vals['relation'] = relation
        elif vals['attribute_type'] == 'multiselect':
            vals['ttype'] = 'many2many'
            vals['relation'] = relation
            vals['serialized'] = True
        else:
            vals['ttype'] = vals['attribute_type']

        if vals.get('serialized'):
            field_obj = self.pool.get('ir.model.fields')
            serialized_ids = field_obj.search([
                ('ttype', '=', 'serialized'),
                ('model_id', '=', vals['model_id']),
                ('name', '=', 'x_custom_json_attrs')])
            if serialized_ids:
                vals['serialization_field_id'] = serialized_ids[0]
            else:
                f_vals = {
                    'name': u'x_custom_json_attrs',
                    # 'field_description': u'Serialized JSON Attributes',
                    'ttype': 'serialized',
                    'model_id': vals['model_id'],
                }
                vals['serialization_field_id'] = field_obj.create(
                    f_vals, {'manual': True})
        vals['state'] = 'manual'
        return super(AttributeAttribute, self).create(vals)

    @api.onchange('field_description')
    def onchange_field_description(self):
        name = self.name or u'x_'
        if self.field_description and not self.create_date:
            name = unicode('x_' + safe_column_name(self.field_description))
        self.name = name

    @api.onchange('name')
    def onchange_name(self):
        res = {}
        if not self.name.startswith('x_'):
            name = u'x_%s' % self.name
        else:
            name = u'%s' % self.name
        res = {'value': {'name': unidecode(name)}}

        context = self._context
        model_name = context.get('force_model')
        if not model_name:
            model_id = context.get('default_model_id')
            if model_id:
                model = self.env['ir.model'].browse(model_id)
                model_name = model.model
        if model_name:
            model_obj = self.env[model_name]
            allowed_model = [x for x in model_obj._inherits] + [model_name]
            res['domain'] = {'model_id': [['model', 'in', allowed_model]]}

        return res


class AttributeGroup(models.Model):
    _name = "attribute.group"
    _description = "Attribute Group"
    _order = "sequence"

    @api.model
    def _get_default_model(self):
        context = self._context
        if context and context.get('force_model'):
            model_id = self.env['ir.model'].search(
                [['model', '=', context['force_model']]])
            if model_id:
                return model_id[0]
        return False

    name = fields.Char(
        size=128,
        required=True,
        translate=True)
    sequence = fields.Integer()
    attribute_set_id = fields.Many2one(
        comodel_name='attribute.set',
        string='Attribute Set')
    attribute_ids = fields.One2many(
        comodel_name='attribute.location',
        inverse_name='attribute_group_id',
        string='Attributes')
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        required=True,
        default=_get_default_model
    )

    @api.model
    def create(self, vals):
        for attribute in vals.get('attribute_ids', []):
            if (vals.get('attribute_set_id') and attribute[2] and
                    not attribute[2].get('attribute_set_id')):
                attribute[2]['attribute_set_id'] = vals['attribute_set_id']
        return super(AttributeGroup, self).create(vals)


class AttributeSet(models.Model):
    _name = "attribute.set"
    _description = "Attribute Set"

    @api.model
    def _get_default_model(self):
        context = self._context
        if context and context.get('force_model'):
            model_id = self.env['ir.model'].search(
                [['model', '=', context['force_model']]])
            if model_id:
                return model_id[0]
        return False

    name = fields.Char(
        size=128,
        required=True,
        translate=True)
    attribute_group_ids = fields.One2many(
        comodel_name='attribute.group',
        inverse_name='attribute_set_id',
        string='Attribute Groups')
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        required=True,
        default=_get_default_model)


class AttributeLocation(models.Model):
    _name = "attribute.location"
    _description = "Attribute Location"
    _order = "sequence"

    attribute_id = fields.Many2one(
        comodel_name='attribute.attribute',
        string='Product Attribute',
        required=True,
        delegate=True,
        ondelete="cascade")
    attribute_set_id = fields.Many2one(
        comodel_name='attribute.set',
        related='attribute_group_id.attribute_set_id',
        string='Attribute Set',
    )
    attribute_group_id = fields.Many2one(
        comodel_name='attribute.group',
        string='Attribute Group',
        required=True)
    sequence = fields.Integer()
