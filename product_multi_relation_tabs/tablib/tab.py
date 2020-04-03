# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from lxml import etree

from odoo import _
from odoo.osv.orm import transfer_modifiers_to_node


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


NAME_PREFIX = 'relation_ids_tab'


class Tab(object):
    """Encapsulate the information on a tab in the database."""

    def __init__(self, tab_record):
        """Create tab from tab_record.

        In this version tab_record can be assumed to be a product.relation.tab.
        """
        self.tab_record = tab_record
        self.name = tab_record.code

    def get_fieldname(self):
        return '%s_%s' % (NAME_PREFIX, self.tab_record.id)

    def get_visible_fieldname(self):
        return '%s_visible' % self.get_fieldname()

    def create_page(self):
        tab_page = etree.Element('page')
        self._set_page_attrs(tab_page)
        field = etree.Element(
            'field',
            name=self.get_fieldname(),
            context='{'
                    '"default_this_product_id": id,'
                    '"default_tab_id": %d,'
                    '"active_test": False}' % self.tab_record.id)
        tab_page.append(field)
        tree = etree.Element('tree', editable='bottom')
        field.append(tree)
        # Now add fields for the editable tree view in the tab.
        type_field = etree.Element(
            'field',
            name='type_selection_id',
            widget='many2one_clickable')
        type_field.set('domain', repr([('tab_id', '=', self.tab_record.id)]))
        type_field.set('options', repr({'no_create': True}))
        tree.append(type_field)
        other_product_field = etree.Element(
            'field',
            string=_('product'),
            name='other_product_id',
            widget='many2one_clickable')
        other_product_field.set('options', repr({'no_create': True}))
        tree.append(other_product_field)
        tree.append(etree.Element('field', name='date_start'))
        tree.append(etree.Element('field', name='date_end'))
        return tab_page

    def _set_page_attrs(self, tab_page):
        tab_page.set('string', self.tab_record.name)
        attrs = {'invisible': [(self.get_visible_fieldname(), '=', False)]}
        tab_page.set('attrs', repr(attrs))
        transfer_modifiers_to_node(attrs, tab_page)

    def compute_visibility(self, product):
        """Compute visibility, dependent on product and conditions."""
        tab = self.tab_record
        if tab.product_ids:
            return product in tab.product_ids
        if tab.product_type:
            if product.type != tab.product_type:
                return False
        if tab.product_category_id:
            if tab.product_category_id not in product.categ_id:
                return False
        return True
