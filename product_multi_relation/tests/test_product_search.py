# Copyright 2015 Camptocamp SA
# Copyright 2016 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields
from odoo.exceptions import ValidationError

from .test_product_relation_common import TestProductRelationCommon


class TestProductSearch(TestProductRelationCommon):

    def test_search_relation_type(self):
        """Test searching on relation type."""
        relation = self._create_consumable2service_relation()
        products = self.product_model.search([
            ('search_relation_type_id', '=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.product_02_consumable in products)
        products = self.product_model.search([
            ('search_relation_type_id', '!=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.product_01_service in products)
        products = self.product_model.search([
            ('search_relation_type_id', '=', self.type_consumable2service.name)
        ])
        self.assertTrue(self.product_01_service in products)
        self.assertTrue(self.product_02_consumable in products)
        products = self.product_model.search([
            ('search_relation_type_id', '=', 'unknown relation')
        ])
        self.assertFalse(products)
        # Check error with invalid search operator:
        with self.assertRaises(ValidationError):
            products = self.product_model.search([
                ('search_relation_type_id', 'child_of', 'some parent')
            ])

    def test_search_relation_product(self):
        """Test searching on related product."""
        self._create_consumable2service_relation()
        products = self.product_model.search([
            ('search_relation_product_id', '=', self.product_02_consumable.id),
        ])
        self.assertTrue(self.product_01_service in products)

    def test_search_relation_date(self):
        """Test searching on relations valid on a certain date."""
        self._create_consumable2service_relation()
        products = self.product_model.search([
            ('search_relation_date', '=', fields.Date.today()),
        ])
        self.assertTrue(self.product_01_service in products)
        self.assertTrue(self.product_02_consumable in products)

    def test_search_any_product(self):
        """Test searching for product left or right."""
        self._create_consumable2service_relation()
        both_relations = self.relation_all_model.search([
            ('any_product_id', '=', self.product_02_consumable.id),
        ])
        self.assertEqual(len(both_relations), 2)

    def test_search_product_category(self):
        """Test searching for products related to products having category."""
        relation_ngo_volunteer = self.relation_all_model.create({
            'this_product_id': self.product_03_ngo.id,
            'type_selection_id': self.selection_ngo2volunteer.id,
            'other_product_id': self.product_04_volunteer.id,
        })
        self.assertTrue(relation_ngo_volunteer)
        products = self.product_model.search([
            ('search_relation_product_categ_id', '=',
             self.category_02_volunteer.id)
        ])
        self.assertTrue(self.product_03_ngo in products)
