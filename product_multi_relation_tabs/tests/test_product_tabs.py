# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from lxml import etree

from odoo.exceptions import ValidationError

from . import common
from ..tablib import Tab


class TestProductTabs(common.TestCommon):
    post_install = True

    def test_create_tab(self):
        self.assertTrue(bool(self.tab_installation_services))
        tab_obj = Tab(self.tab_installation_services)
        # fields_view_get should force the creation of the new tabs.
        view_product_form = self.env.ref('base.view_product_form')
        view = self.product_model.with_context().fields_view_get(
            view_id=view_product_form.id, view_type='form')
        # The form view for product should now also contain field 'id'.
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="id"]')
        self.assertTrue(field, 'Id field does not exist.')
        # There should now be a field in product for the new tab.
        fieldname = tab_obj.get_fieldname()
        self.assertTrue(fieldname in self.product_model._fields)
        # And we should have a field for the tab:
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertTrue(
            field,
            'Tab field %s does not exist in %s.' %
            (fieldname, etree.tostring(tree)))
        # There should be no effect on the tree view:
        view = self. product_model.with_context().fields_view_get(
            view_type='tree')
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertFalse(
            field,
            'Tab field %s should not exist in %s.' %
            (fieldname, etree.tostring(tree)))

    def test_view_without_pages(self):
        """Check that _add_tab_pages does not effect view without pages."""
        # pylint: disable=protected-access
        view = etree.Element('view')
        extra_fields = self.product_model._add_tab_pages(view)
        self.assertFalse(extra_fields)

    def test_tab_modifications(self):
        tab_services = self.tab_model.create({
            'code': 'services',
            'name': 'Services'})
        self.assertTrue(bool(tab_services))
        type_service = self.type_model.create({
            'name': 'uses service',
            'name_inverse': 'used by',
            'product_type_left': 'service',  # This emulates a user mistake.
            'product_type_right': 'service',
            'tab_left_id': tab_services.id})
        self.assertTrue(bool(type_service))
        # If we change tab now to be only valid on products
        # the tab_left_id field should be cleared from the type:
        tab_services.write({'product_type': 'consu'})
        self.assertFalse(type_service.tab_left_id.id)
        # Trying to set the tab back on type should be impossible:
        with self.assertRaises(ValidationError):
            type_service.write({'tab_left_id': tab_services.id})
        # We should be able to change tab, if also changing product type.
        type_service.write({
            'product_type_left': 'consu',
            'tab_left_id': tab_services.id})
        self.assertEqual(
            type_service.tab_left_id.id,
            tab_services.id)
        # Unlinking the tab should reset the tab_left_id on relation type.
        tab_services.unlink()
        self.assertEqual(
            type_service.tab_left_id.id,
            False)
        # It should not be possible to add category or product type to as
        # selection criteria to a tab meant for specific products.
        with self.assertRaises(ValidationError):
            self.tab_spares.write({'product_type': 'consu'})
        with self.assertRaises(ValidationError):
            self.tab_spares.write({
                'product_category_id': self.category_machine.id})

    def test_type_modifications(self):
        self.assertTrue(bool(self.tab_installation_services))
        self.assertTrue(bool(self.tab_supported_machines))
        self.assertTrue(bool(self.type_service))
        # Trying to clear either category should raise ValidationError:
        with self.assertRaises(ValidationError):
            self.type_service.write({'product_category_left': False})
        with self.assertRaises(ValidationError):
            self.type_service.write({'product_category_right': False})
        # Trying to clear either product type should raise ValidationError:
        with self.assertRaises(ValidationError):
            self.type_service.write({'product_type_left': False})
        with self.assertRaises(ValidationError):
            self.type_service.write({'product_type_right': False})

    def test_relations(self):
        """Test relations shown on tab."""
        relation_all_model = self.env['product.relation.all']
        self.assertTrue(bool(self.tab_installation_services))
        self.assertTrue(bool(self.type_machine_is_installed_using))
        self.assertTrue(bool(self.product_machine))
        self.assertTrue(bool(self.product_basic_is))
        self.assertTrue(bool(self.relation_m1_bis))
        # Now we should be able to find the relation with the tab_id:
        machine_services = relation_all_model.search([
            ('tab_id', '=', self.tab_installation_services.id)])
        self.assertTrue(bool(machine_services))
        self.assertIn(
            self.product_machine,
            [relation.this_product_id for relation in machine_services])
        # We should find the company on the product through tab field:
        tab_obj = Tab(self.tab_installation_services)
        fieldname = tab_obj.get_fieldname()
        self.assertTrue(fieldname in self.product_model._fields)
        machine_services = self.product_machine[fieldname]
        self.assertEqual(len(machine_services), 1)
        self.assertEqual(
            machine_services.other_product_id.id,
            self.product_basic_is.id)
        #  When adding a new relation on a tab, type must be for tab.
        onchange_result = machine_services.with_context(
            default_tab_id=self.tab_installation_services.id
        ).onchange_product_id()
        self.assertTrue(onchange_result)
        self.assertIn('domain', onchange_result)
        self.assertIn('type_selection_id', onchange_result['domain'])
        self.assertEqual(
            onchange_result['domain']['type_selection_id'][-1],
            ('tab_id', '=', self.tab_installation_services.id))

    def test_compute_visibility(self):
        """Check the computation of visibility on products."""
        # pylint: disable=protected-access
        main_product = self.env.ref('base.main_product')
        main_product._compute_tabs_visibility()
        tab_obj = Tab(self.tab_spares)
        fieldname = tab_obj.get_fieldname()
        visible_fieldname = tab_obj.get_visible_fieldname()
        self.assertIn(visible_fieldname, main_product._fields)
        self.assertIn(fieldname, main_product._fields)
        self.assertEqual(main_product[visible_fieldname], True)
        department_relations = main_product[fieldname]
        self.assertTrue(len(department_relations) >= 1)
        departments = [
            relation.other_product_id for relation in department_relations]
        for department in departments:
            self.assertIn(
                self.category_spare, department.category_id)
