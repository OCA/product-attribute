# Copyright 2016-2017 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError

from .test_product_relation_common import TestProductRelationCommon


class TestProductRelation(TestProductRelationCommon):

    post_install = True

    def test_selection_name_search(self):
        """Test wether we can find type selection on reverse name."""
        selection_types = self.selection_model.name_search(
            name=self.selection_service2consumable.name)
        self.assertTrue(selection_types)
        self.assertTrue(
            (self.selection_service2consumable.id,
             self.selection_service2consumable.name) in selection_types)

    def test_self_allowed(self):
        """Test creation of relation to same product when type allows."""
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': True})
        self.assertTrue(type_allow)
        reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id})
        self.assertTrue(reflexive_relation)

    def test_self_disallowed(self):
        """Test creating relation to same product when disallowed.

        Attempt to create a relation of a product to the same product should
        raise an error when the type of relation explicitly disallows this.
        """
        type_disallow = self.type_model.create({
            'name': 'disallow',
            'name_inverse': 'disallow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': False})
        self.assertTrue(type_disallow)
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': type_disallow.id,
                'left_product_id': self.product_01_service.id,
                'right_product_id': self.product_01_service.id})

    def test_self_disallowed_after_self_relation_created(self):
        """Test that allow_self can not be true if a reflexive relation already exists.

        If at least one reflexive relation exists for the given type,
        reflexivity can not be disallowed.
        """
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': True})
        self.assertTrue(type_allow)
        reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id})
        self.assertTrue(reflexive_relation)
        with self.assertRaises(ValidationError):
            type_allow.allow_self = False

    def test_self_disallowed_with_delete_invalid_relations(self):
        """Test handle_invalid_onchange delete with allow_self disabled.

        When deactivating allow_self, if handle_invalid_onchange is set
        to delete, then existing reflexive relations are deleted.

        Non reflexive relations are not modified.
        """
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': True,
            'handle_invalid_onchange': 'delete',
        })
        reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id,
        })
        normal_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_04_volunteer.id,
        })

        type_allow.allow_self = False
        self.assertFalse(reflexive_relation.exists())
        self.assertTrue(normal_relation.exists())

    def test_self_disallowed_with_end_invalid_relations(self):
        """Test handle_invalid_onchange delete with allow_self disabled.

        When deactivating allow_self, if handle_invalid_onchange is set
        to end, then active reflexive relations are ended.

        Non reflexive relations are not modified.

        Reflexive relations with an end date prior to the current date
        are not modified.
        """
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': True,
            'handle_invalid_onchange': 'end',
        })
        reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id,
            'date_start': '2000-01-02',
        })
        past_reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id,
            'date_end': '2000-01-01',
        })
        normal_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_04_volunteer.id,
        })

        type_allow.allow_self = False
        self.assertEqual(reflexive_relation.date_end, fields.Date.today())
        self.assertEqual(past_reflexive_relation.date_end, date(2000, 1, 1))
        self.assertFalse(normal_relation.date_end)

    def test_self_disallowed_with_future_reflexive_relation(self):
        """Test future reflexive relations are deleted.

        If handle_invalid_onchange is set to end, then deactivating
        reflexivity will delete invalid relations in the future.
        """
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'product_type_left': 's',
            'product_type_right': 's',
            'allow_self': True,
            'handle_invalid_onchange': 'end',
        })
        future_reflexive_relation = self.relation_model.create({
            'type_id': type_allow.id,
            'left_product_id': self.product_01_service.id,
            'right_product_id': self.product_01_service.id,
            'date_start': datetime.now() + timedelta(1),
        })
        type_allow.allow_self = False
        self.assertFalse(future_reflexive_relation.exists())

    def test_self_default(self):
        """Test default not to allow relation with same product.

        Attempt to create a relation of a product to the same product
        raise an error when the type of relation does not explicitly allow
        this.
        """
        type_default = self.type_model.create({
            'name': 'default',
            'name_inverse': 'default_inverse',
            'product_type_left': 's',
            'product_type_right': 's'})
        self.assertTrue(type_default)
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': type_default.id,
                'left_product_id': self.product_01_service.id,
                'right_product_id': self.product_01_service.id})

    def test_self_mixed(self):
        """Test creation of relation with wrong types.

        Trying to create a relation between products with an inappropiate
        type should raise an error.
        """
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_consumable2service.id,
                'left_product_id': self.product_01_service.id,
                'right_product_id': self.product_02_consumable.id})

    def test_symmetric(self):
        """Test creating symmetric relation."""
        # Start out with non symmetric relation:
        type_symmetric = self.type_model.create({
            'name': 'not yet symmetric',
            'name_inverse': 'the other side of not symmetric',
            'is_symmetric': False,
            'product_type_left': False,
            'product_type_right': 's'})
        # not yet symmetric relation should result in two records in
        # selection:
        selection_symmetric = self.selection_model.search([
            ('type_id', '=', type_symmetric.id)])
        self.assertEqual(len(selection_symmetric), 2)
        # Now change to symmetric and test name and inverse name:
        with self.env.do_in_draft():
            type_symmetric.write({
                'name': 'sym',
                'is_symmetric': True})
        self.assertEqual(type_symmetric.is_symmetric, True)
        self.assertEqual(
            type_symmetric.name_inverse,
            type_symmetric.name)
        self.assertEqual(
            type_symmetric.product_type_right,
            type_symmetric.product_type_left)
        # now update the database:
        type_symmetric.write({
            'name': type_symmetric.name,
            'is_symmetric': type_symmetric.is_symmetric,
            'name_inverse': type_symmetric.name_inverse,
            'product_type_right': type_symmetric.product_type_right})
        # symmetric relation should result in only one record in
        # selection:
        selection_symmetric = self.selection_model.search([
            ('type_id', '=', type_symmetric.id)])
        self.assertEqual(len(selection_symmetric), 1)
        relation = self.relation_all_model.create({
            'type_selection_id': selection_symmetric.id,
            'this_product_id': self.product_02_consumable.id,
            'other_product_id': self.product_01_service.id})
        products = self.product_model.search([
            ('search_relation_type_id', '=', relation.type_selection_id.id)])
        self.assertTrue(self.product_01_service in products)
        self.assertTrue(self.product_02_consumable in products)

    def test_category_domain(self):
        """Test check on category in relations."""
        # Check on left side:
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_ngo2volunteer.id,
                'left_product_id': self.product_02_consumable.id,
                'right_product_id': self.product_04_volunteer.id})
        # Check on right side:
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_ngo2volunteer.id,
                'left_product_id': self.product_03_ngo.id,
                'right_product_id': self.product_01_service.id})

    def test_relation_type_change(self):
        """Test change in relation type conditions."""
        # First create a relation type having no particular conditions.
        (type_school2student,
         school2student,
         school2student_inverse) = \
            self._create_relation_type_selection({
                'name': 'school has student',
                'name_inverse': 'studies at school'})
        # Second create relations based on those conditions.
        product_school = self.product_model.create({
            'name': 'Test School',
            'is_consumable': True,
            'ref': 'TS'})
        product_bart = self.product_model.create({
            'name': 'Bart Simpson',
            'is_consumable': False,
            'ref': 'BS'})
        product_lisa = self.product_model.create({
            'name': 'Lisa Simpson',
            'is_consumable': False,
            'ref': 'LS'})
        relation_school2bart = self.relation_all_model.create({
            'this_product_id': product_school.id,
            'type_selection_id': school2student.id,
            'other_product_id': product_bart.id})
        self.assertTrue(relation_school2bart)
        relation_school2lisa = self.relation_all_model.create({
            'this_product_id': product_school.id,
            'type_selection_id': school2student.id,
            'other_product_id': product_lisa.id})
        self.assertTrue(relation_school2lisa)
        relation_bart2lisa = self.relation_all_model.create({
            'this_product_id': product_bart.id,
            'type_selection_id': school2student.id,
            'other_product_id': product_lisa.id})
        self.assertTrue(relation_bart2lisa)
        # Third creata a category and make it a condition for the
        #     relation type.
        # - Test restriction
        # - Test ignore
        category_student = self.category_model.create({'name': 'Student'})
        with self.assertRaises(ValidationError):
            type_school2student.write({
                'product_category_right': category_student.id})
        self.assertFalse(type_school2student.product_category_right.id)
        type_school2student.write({
            'handle_invalid_onchange': 'ignore',
            'product_category_right': category_student.id})
        self.assertEqual(
            type_school2student.product_category_right.id,
            category_student.id)
        # Fourth make consumable type a condition for left product
        # - Test ending
        # - Test deletion
        product_bart.write({
            'category_id': [(4, category_student.id)]})
        product_lisa.write({
            'category_id': [(4, category_student.id)]})
        # Future student to be deleted by end action:
        product_homer = self.product_model.create({
            'name': 'Homer Simpson',
            'is_consumable': False,
            'ref': 'HS',
            'category_id': [(4, category_student.id)]})
        relation_lisa2homer = self.relation_all_model.create({
            'this_product_id': product_lisa.id,
            'type_selection_id': school2student.id,
            'other_product_id': product_homer.id,
            'date_start': date.today() + relativedelta(months=+6)})
        self.assertTrue(relation_lisa2homer)
        type_school2student.write({
            'handle_invalid_onchange': 'end',
            'product_type_left': 'c'})
        self.assertEqual(
            relation_bart2lisa.date_end,
            fields.Date.today())
        self.assertFalse(relation_lisa2homer.exists())
        type_school2student.write({
            'handle_invalid_onchange': 'delete',
            'product_type_left': 'c',
            'product_type_right': 's'})
        self.assertFalse(relation_bart2lisa.exists())

    def test_relation_type_unlink(self):
        """Test delete of relation type, including deleting relations."""
        # First create a relation type having restrict particular conditions.
        type_model = self.env['product.relation.type']
        relation_model = self.env['product.relation']
        product_model = self.env['product.template']
        type_school2student = type_model.create({
            'name': 'school has student',
            'name_inverse': 'studies at school',
            'handle_invalid_onchange': 'delete'})
        # Second create relation based on those conditions.
        product_school = product_model.create({
            'name': 'Test School',
            'is_consumable': True,
            'ref': 'TS'})
        product_bart = product_model.create({
            'name': 'Bart Simpson',
            'is_consumable': False,
            'ref': 'BS'})
        relation_school2bart = relation_model.create({
            'left_product_id': product_school.id,
            'type_id': type_school2student.id,
            'right_product_id': product_bart.id})
        # Delete type. Relations with type should also cease to exist:
        type_school2student.unlink()
        self.assertFalse(relation_school2bart.exists())
