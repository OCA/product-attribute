# Copyright 2016-2017 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date
from odoo.exceptions import ValidationError

from .test_product_relation_common import TestProductRelationCommon


class TestProductRelation(TestProductRelationCommon):

    def setUp(self):
        super(TestProductRelation, self).setUp()

        # Create a new relation type which will not have valid relations:
        category_nobody = self.category_model.create({
            'name': 'Nobody'})
        (self.type_nobody,
         self.selection_nobody,
         self.selection_nobody_inverse) = (
            self._create_relation_type_selection({
                'name': 'has relation with nobody',
                'name_inverse': 'nobody has relation with',
                'product_type_left': 'c',
                'product_type_right': 's',
                'product_category_left': category_nobody.id,
                'product_category_right': category_nobody.id}))

    def _get_empty_relation(self):
        """Get empty relation record for onchange tests."""
        # Need English, because we will compare text
        return self.relation_all_model.with_context(lang='en_US').new({})

    def test_get_product_types(self):
        """Product types should contain at least 'c' and 's'."""
        product_types = self.selection_model.get_product_types()
        type_codes = [ptype[0] for ptype in product_types]
        self.assertTrue('c' in type_codes)
        self.assertTrue('s' in type_codes)

    def test_create_with_active_id(self):
        """Test creation with this_product_id from active_id."""
        # Check wether we can create connection from consumable to service,
        # taking the particular consumable from the active records:
        relation = self.relation_all_model.with_context(
            active_id=self.product_02_consumable.id,
            active_ids=self.product_02_consumable.ids).create({
                'other_product_id': self.product_01_service.id,
                'type_selection_id': self.selection_consumable2service.id})
        self.assertTrue(relation)
        self.assertEqual(relation.this_product_id, self.product_02_consumable)
        # Product should have one relation now:
        self.assertEqual(self.product_01_service.relation_count, 1)
        # Test create without type_selection_id:
        with self.assertRaises(ValidationError):
            self.relation_all_model.create({
                'this_product_id': self.product_02_consumable.id,
                'other_product_id': self.product_01_service.id})

    def test_display_name(self):
        """Test display name"""
        relation = self._create_consumable2service_relation()
        self.assertEqual(
            relation.display_name, '%s %s %s' % (
                relation.this_product_id.name,
                relation.type_selection_id.name,
                relation.other_product_id.name))

    def test__regular_write(self):
        """Test write with valid data."""
        relation = self._create_consumable2service_relation()
        relation.write({'date_start': '2014-09-01'})
        relation.invalidate_cache(ids=relation.ids)
        self.assertEqual(relation.date_start, date(2014, 9, 1))

    def test_write_incompatible_dates(self):
        """Test write with date_end before date_start."""
        relation = self._create_consumable2service_relation()
        with self.assertRaises(ValidationError):
            relation.write({
                'date_start': '2016-09-01',
                'date_end': '2016-08-01'})

    def test_validate_overlapping_01(self):
        """Test create overlapping with no start / end dates."""
        relation = self._create_consumable2service_relation()
        with self.assertRaises(ValidationError):
            # New relation with no start / end should give error
            self.relation_all_model.create({
                'this_product_id': relation.this_product_id.id,
                'type_selection_id': relation.type_selection_id.id,
                'other_product_id': relation.other_product_id.id})

    def test_validate_overlapping_02(self):
        """Test create overlapping with start / end dates."""
        relation = self.relation_all_model.create({
            'this_product_id': self.product_02_consumable.id,
            'type_selection_id': self.selection_consumable2service.id,
            'other_product_id': self.product_01_service.id,
            'date_start': '2015-09-01',
            'date_end': '2016-08-31'})
        # New relation with overlapping start / end should give error
        with self.assertRaises(ValidationError):
            self.relation_all_model.create({
                'this_product_id': relation.this_product_id.id,
                'type_selection_id': relation.type_selection_id.id,
                'other_product_id': relation.other_product_id.id,
                'date_start': '2016-08-01',
                'date_end': '2017-07-30'})

    def test_validate_overlapping_03(self):
        """Test create not overlapping."""
        relation = self.relation_all_model.create({
            'this_product_id': self.product_02_consumable.id,
            'type_selection_id': self.selection_consumable2service.id,
            'other_product_id': self.product_01_service.id,
            'date_start': '2015-09-01',
            'date_end': '2016-08-31'})
        relation_another_record = self.relation_all_model.create({
            'this_product_id': relation.this_product_id.id,
            'type_selection_id': relation.type_selection_id.id,
            'other_product_id': relation.other_product_id.id,
            'date_start': '2016-09-01',
            'date_end': '2017-08-31'})
        self.assertTrue(relation_another_record)

    def test_inverse_record(self):
        """Test creation of inverse record."""
        relation = self._create_consumable2service_relation()
        inverse_relation = self.relation_all_model.search([
            ('this_product_id', '=', relation.other_product_id.id),
            ('other_product_id', '=', relation.this_product_id.id)])
        self.assertEqual(len(inverse_relation), 1)
        self.assertEqual(
            inverse_relation.type_selection_id.name,
            self.selection_service2consumable.name)

    def test_inverse_creation(self):
        """Test creation of record through inverse selection."""
        relation = self.relation_all_model.create({
            'this_product_id': self.product_01_service.id,
            'type_selection_id': self.selection_service2consumable.id,
            'other_product_id': self.product_02_consumable.id})
        # Check wether display name is what we should expect:
        self.assertEqual(
            relation.display_name, '%s %s %s' % (
                self.product_01_service.name,
                self.selection_service2consumable.name,
                self.product_02_consumable.name))

    def test_inverse_creation_type_id(self):
        """Test creation of record through inverse selection with type_id."""
        relation = self.relation_all_model.create({
            'this_product_id': self.product_01_service.id,
            'type_id': self.selection_service2consumable.type_id.id,
            'is_inverse': True,
            'other_product_id': self.product_02_consumable.id})
        # Check wether display name is what we should expect:
        self.assertEqual(
            relation.display_name, '%s %s %s' % (
                self.product_01_service.name,
                self.selection_service2consumable.name,
                self.product_02_consumable.name))

    def test_unlink(self):
        """Unlinking derived relation should unlink base relation."""
        # Check wether underlying record is removed when record is removed:
        relation = self._create_consumable2service_relation()
        base_model = self.env[relation.res_model]
        base_relation = base_model.browse([relation.res_id])
        relation.unlink()
        self.assertFalse(base_relation.exists())

    def test_on_change_type_selection(self):
        """Test on_change_type_selection."""
        # 1. Test call with empty relation
        relation_empty = self._get_empty_relation()
        result = relation_empty.onchange_type_selection_id()
        self.assertTrue('domain' in result)
        self.assertFalse('warning' in result)
        self.assertTrue('this_product_id' in result['domain'])
        self.assertFalse(result['domain']['this_product_id'])
        self.assertTrue('other_product_id' in result['domain'])
        self.assertFalse(result['domain']['other_product_id'])
        # 2. Test call with consumable 2 service relation
        relation = self._create_consumable2service_relation()
        domain = relation.onchange_type_selection_id()['domain']
        self.assertTrue(
            ('is_consumable', '=', False) in domain['other_product_id'])
        # 3. Test with relation needing categories,
        #    take active product from active_id:
        relation_ngo_volunteer = self.relation_all_model.with_context(
            active_id=self.product_03_ngo.id).create({
                'type_selection_id': self.selection_ngo2volunteer.id,
                'other_product_id': self.product_04_volunteer.id})
        domain = relation_ngo_volunteer.onchange_type_selection_id()['domain']
        self.assertTrue(
            ('category_id', 'in', [self.category_01_ngo.id]) in
            domain['this_product_id'])
        self.assertTrue(
            ('category_id', 'in', [self.category_02_volunteer.id]) in
            domain['other_product_id'])
        # 4. Test with invalid or impossible combinations
        relation_nobody = self._get_empty_relation()
        with self.env.do_in_draft():
            relation_nobody.type_selection_id = self.selection_nobody
        warning = relation_nobody.onchange_type_selection_id()['warning']
        self.assertTrue('message' in warning)
        self.assertTrue('No this product available' in warning['message'])
        with self.env.do_in_draft():
            relation_nobody.this_product_id = self.product_02_consumable
        warning = relation_nobody.onchange_type_selection_id()['warning']
        self.assertTrue('message' in warning)
        self.assertTrue('incompatible' in warning['message'])
        # Allow left product and check message for other product:
        self.type_nobody.write({'product_category_left': False})
        self.selection_nobody.invalidate_cache(ids=self.selection_nobody.ids)
        warning = relation_nobody.onchange_type_selection_id()['warning']
        self.assertTrue('message' in warning)
        self.assertTrue('No other product available' in warning['message'])

    def test_on_change_product_id(self):
        """Test on_change_product_id."""
        # 1. Test call with empty relation
        relation_empty = self._get_empty_relation()
        result = relation_empty.onchange_product_id()
        self.assertTrue('domain' in result)
        self.assertFalse('warning' in result)
        self.assertTrue('type_selection_id' in result['domain'])
        self.assertFalse(result['domain']['type_selection_id'])
        # 2. Test call with consumable 2 service relation
        relation = self._create_consumable2service_relation()
        domain = relation.onchange_product_id()['domain']
        self.assertTrue(
            ('product_type_this', '=', 'c') in domain['type_selection_id'])
        # 3. Test with invalid or impossible combinations
        relation_nobody = self._get_empty_relation()
        with self.env.do_in_draft():
            relation_nobody.this_product_id = self.product_02_consumable
            relation_nobody.type_selection_id = self.selection_nobody
        warning = relation_nobody.onchange_product_id()['warning']
        self.assertTrue('message' in warning)
        self.assertTrue('incompatible' in warning['message'])

    def test_write(self):
        """Test write. Special attention for changing type."""
        relation_consumable2service = self._create_consumable2service_relation()
        consumable_product = relation_consumable2service.this_product_id
        # First get another worker:
        product_extra_service = self.product_model.create({
            'name': 'A new worker',
            'is_consumable': False,
            'ref': 'NW01'})
        relation_consumable2service.write({
            'other_product_id': product_extra_service.id})
        self.assertEqual(
            relation_consumable2service.other_product_id.name,
            product_extra_service.name)
        # We will also change to a type going from service to consumable:
        (type_worker2consumable,
         selection_worker2consumable,
         selection_consumable2worker) = self._create_relation_type_selection({
             'name': 'works for',
             'name_inverse': 'has worker',
             'product_type_left': 's',
             'product_type_right': 'c'})
        relation_consumable2service.write({
            'this_product_id': product_extra_service.id,
            'type_selection_id': selection_worker2consumable.id,
            'other_product_id': consumable_product.id})
        self.assertEqual(
            relation_consumable2service.this_product_id.id,
            product_extra_service.id)
        self.assertEqual(
            relation_consumable2service.type_selection_id.id,
            selection_worker2consumable.id)
        self.assertEqual(
            relation_consumable2service.other_product_id.id,
            consumable_product.id)
