# Copyright 2016 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestProductRelationCommon(common.TransactionCase):

    def setUp(self):
        super(TestProductRelationCommon, self).setUp()

        self.product_model = self.env['product.template']
        self.category_model = self.env['product.category']
        self.type_model = self.env['product.relation.type']
        self.selection_model = self.env['product.relation.type.selection']
        self.relation_model = self.env['product.relation']
        self.relation_all_model = self.env['product.relation.all']
        self.product_01_service = self.product_model.create({
            'name': 'Test Service 1',
            'type': 'service',
            'default_code': 'SV01'})
        self.product_02_consumable = self.product_model.create({
            'name': 'Test Consumable',
            'type': 'consu',
            'default_code': 'CO02'})
        # Create products with specific categories:
        self.category_01_sd = self.category_model.create({
            'name': 'Supportable Device'})
        self.product_03_cat_sd = self.product_model.create({
            'name': 'Test Consumable with Category',
            'type': 'consu',
            'default_code': 'CO03',
            'categ_id': self.category_01_sd.id})
        self.category_02_ss = self.category_model.create({
            'name': 'Support Service'})
        self.product_04_cat_ss = self.product_model.create({
            'name': 'Test Service with Category',
            'type': 'service',
            'default_code': 'SV04',
            'categ_id': self.category_02_ss.id})
        # Create a new relation type without categories:
        (self.type_consumable2service,
         self.selection_consumable2service,
         self.selection_service2consumable) = \
            self._create_relation_type_selection({
                'name': 'mixed',
                'name_inverse': 'mixed_inverse',
                'product_type_left': 'consu',
                'product_type_right': 'service'})
        # Create a new relation type with categories:
        (self.type_sd2ss,
         self.selection_sd2ss,
         self.selection_ss2sd) = \
            self._create_relation_type_selection({
                'name': 'is supported by',
                'name_inverse': 'supports',
                'product_type_left': 'consu',
                'product_type_right': 'service',
                'product_category_left': self.category_01_sd.id,
                'product_category_right': self.category_02_ss.id})

    def _create_relation_type_selection(self, vals):
        """Create relation type and return this with selection types."""
        assert 'name' in vals, (
            "Name missing in vals to create relation type. Vals: %s."
            % vals)
        assert 'name' in vals, (
            "Name_inverse missing in vals to create relation type. Vals: %s."
            % vals)
        new_type = self.type_model.create(vals)
        self.assertTrue(
            new_type,
            msg="No relation type created with vals %s." % vals)
        selection_types = self.selection_model.search([
            ('type_id', '=', new_type.id)])
        for st in selection_types:
            if st.is_inverse:
                inverse_type_selection = st
            else:
                type_selection = st
        self.assertTrue(
            inverse_type_selection,
            msg="Failed to find inverse type selection based on"
                " relation type created with vals %s." % vals)
        self.assertTrue(
            type_selection,
            msg="Failed to find type selection based on"
                " relation type created with vals %s." % vals)
        return (new_type, type_selection, inverse_type_selection)

    def _create_consumable2service_relation(self):
        """Utility function to get a relation from consumable 2 product."""
        return self.relation_all_model.create({
            'type_selection_id': self.selection_consumable2service.id,
            'this_product_id': self.product_02_consumable.id,
            'other_product_id': self.product_01_service.id})
