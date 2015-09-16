# coding: utf-8
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
###############################################################################
#    Credits:
#    Coded by: Katherine Zaoral <kathy@vauxoo.com>
#    Planified by: Nhomar Hernandez <nhomar@vauxoo.com>
#    Audited by: Nhomar Hernandez <nhomar@vauxoo.com>
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from openerp.tests import common
from openerp import exceptions
import time


class TestProductLifecycle(common.TransactionCase):

    """
    - CRUD Tests over product.product
    - Purchase Order with discontinued lines.
    - Replacement Products Wizard Test

        (sellable) with 0 replacement
        (sellable) with 1 replacement (sellable)
        (sellable) with 1 replacement (obsolete)
        (sellable) with 1 replacement (end)
        (sellable) with 1 replacement (draft)
        (sellable) with 2 replacement (sellable, sellable)
        (sellable) with 2 replacement (sellable, draft)
        (sellable) with 2 replacement (sellable, end)
        (sellable) with 2 replacement (sellable, obsolete)
        (sellable) with 2 replacement (obsolete, obsolete)

        Product Template: iPad Retina Display


        Replacements:

        (sellable,           [sellable, obsolete])
        (product_product_4c, [product_product_4g product_product_4f])

        (draft,              [sellable, end])
        (product_product_4,  [product_product_4e])

        (obsolete,           [end])
        (product_product_4b, [product_product_4e])

        (sellable (na),      [obsolete])
        (product_product_4d, product_product_4f)


        model="product.product"
        xml_id                      code   attributes           state
        product.product_product_4   A2323  16 GB, White, Wi-Fi  draft
        product.product_product_4b  A2324  16 GB, Black, Wi-Fi  obsolete
        product.product_product_4c  A2325  32 GB, White, Wi-Fi  sellable
        product.product_product_4d  A2326  32 GB, Black, Wi-Fi  sellable (na)
                product_product_4e  A2327  16 GB, Gray,  Wi-Fi  end
                product_product_4f  A2328  32 GB, Gray,  Wi-Fi  obsolete
                product_product_4g  A2329  32 GB, Red,   Wi-Fi  sellable


        model="product.attribute.value"
        xml_id                        attribute_id  name
        product.product_attribute_value_1   Memory        16 GB
        product.product_attribute_value_2   Memory        32 GB
        product.product_attribute_value_3   Color         Withe
        product.product_attribute_value_4   Color         Black
               .product_attribute_value_6   Color         Gray
               .product_attribute_value_7   Color         Red
        product.product_attribute_value_5   Wi-FI         2.4 Ghz
    """

    def setUp(self):
        """ Add global varaible for the model and xml id record used  """
        super(TestProductLifecycle, self).setUp()
        self.sellable_product = self.ref('product.product_product_4c')
        self.obsolete_product = self.ref('product.product_product_4b')
        self.draft_product = self.ref('product.product_product_4')
        self.sellable_replacement = self.ref(
            'product_lifecycle.product_product_4g')
        self.obsolete_replacement = self.ref(
            'product_lifecycle.product_product_4f')
        self.product_obj = self.env['product.product']
        self.order_obj = self.env['purchase.order']
        self.imd_obj = self.env['ir.model.data']
        self.wiz_obj = self.env['replacement.product']

    def create_product(self):
        """ Create a new product """
        product = self.product_obj.create({
            "default_code": 'A2330',
            "product_tmpl_id":
            self.ref("product.product_product_4_product_template"),
            "attribute_value_ids": [(6, 0, [
                self.ref('product.product_attribute_value_1'),
                self.ref('product_lifecycle.product_attribute_value_6'),
                self.ref('product.product_attribute_value_5')])],
            "replacement_product_ids": [(
                6, 0, [self.ref('product_lifecycle.product_product_4e')]
            )]})
        return product

    def create_pol(self, order, product):
        """
        Create a new purchase order line for the given purchase order taking
        as input only the product
        """
        order.write({
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_qty': 10.0,
                'product_uom': product.uom_id.id,
                'price_unit': product.price,
                'name': product.name_template,
                'sequence': len(order.order_line) + 1,
                'date_planned': time.strftime('%Y-%m-%d')
            })]})

    def create_po(self):
        """ Create a purchase order """
        pricelist_id = 1
        partner_id = self.ref('base.res_partner_1')
        order = self.order_obj.create({
            'partner_id': partner_id,
            'location_id': self.ref('stock.stock_location_stock'),
            'pricelist_id': pricelist_id})
        return order

    def test_01_product_create(self):
        """
        Create a new product and check it was correctly with the default
        product lifecycle state and the replacements products were link.
        """
        # Create new product with a replacement product
        product = self.create_product()

        # Check recently was created product with default 'In Development'
        # value state and that the replacement was assigned. This case also
        # check the read test.
        self.assertTrue(product)
        self.assertEqual(product.state2, 'draft')
        self.assertTrue(product.replacement_product_ids)
        self.assertEqual(len(product.replacement_product_ids), 1)
        self.assertEqual(product.replacement_product_ids[0].id,
                         self.ref('product_lifecycle.product_product_4e'))

    def test_02_product_update(self):
        """
        Update the product status. Get an already exist product and update its
        product lifecifle status from draft to sellable.
        """
        # Update new product state2 from default draft to sellable
        new_product = self.create_product()
        self.assertEqual(new_product.state2, 'draft')
        new_product.state2 = 'sellable'
        self.assertEqual(new_product.state2, 'sellable')

        # Same but to an existing demo product.
        demo_product = self.product_obj.browse(
            self.ref('product_lifecycle.product_product_4g'))
        self.assertEqual(demo_product.state2, 'sellable')
        demo_product.state2 = 'draft'
        self.assertEqual(demo_product.state2, 'draft')

        # Update new product invividual field (field defined in product.product
        # model).
        self.assertEqual(new_product.default_code, 'A2330')
        new_product.default_code = 'A2330-1'
        self.assertEqual(new_product.default_code, 'A2330-1')

        # Same but to an existing demo product.
        self.assertEqual(demo_product.default_code, 'A2329')
        demo_product.default_code = 'A2329-1'
        self.assertEqual(demo_product.default_code, 'A2329-1')

        # Update new product commom characteristic (field defined in
        # product.template) and check that affects the another product
        # variants
        self.assertFalse(new_product.description)
        new_product.description = 'This is a New Product'
        self.assertEqual(new_product.description, 'This is a New Product')
        self.assertEqual(demo_product.description, 'This is a New Product')
        demo_product.description = False
        self.assertFalse(demo_product.description)

    def test_03_product_delete(self):
        """
        Now we are going to delete a recently created product record.
        """
        product = self.create_product()
        products = self.product_obj.search([])
        self.assertIn(product, products)
        product.unlink()
        self.assertNotIn(product.exists(), products)

    def test_04_product_duplicate(self):
        """
        Duplicate product record.
        """
        new_product = self.product_obj.browse(self.obsolete_product).copy()
        self.assertTrue(new_product)
        self.assertEqual(new_product.state2, 'draft')

    def test_05_purchase_order(self):
        """
        Do not let to save a purchase order with discontinued products
        """
        # Create purchase Order and check purchase order was created correctly
        # (without lines)
        order = self.create_po()
        self.assertTrue(order)
        self.assertFalse(order.order_line)

        # Add one sellable line (first line)
        sellable_product = self.product_obj.browse(self.sellable_product)
        self.create_pol(order, sellable_product)
        self.assertTrue(order.order_line)
        self.assertEquals(len(order.order_line), 1)
        self.assertIn(sellable_product, order.order_line.mapped('product_id'))
        self.assertEquals(order.order_line.product_id.state2, 'sellable')

        # Add one draft line (second line)
        draft_product = self.product_obj.browse(self.draft_product)
        self.create_pol(order, draft_product)
        self.assertEquals(len(order.order_line), 2)
        self.assertIn(draft_product, order.order_line.mapped('product_id'))
        self.assertEquals(set(order.order_line.mapped('product_id.state2')),
                          set(['sellable', 'draft']))

        # Add one obsolete line. This will raise an exception.
        obsolete_product = self.product_obj.browse(self.obsolete_product)
        with self.assertRaises(exceptions.Warning):
            self.create_pol(order, obsolete_product)

    def test_06_replacement_product_wizard(self):
        """
        I will take a valid purchase order and I will update one of its
        sellable product to a obsolete product.

        This way when runing the replacement wizard over the purchase order to
        update the line with the obsolete product and check that this is
        working propertly.


         (obsolete,           [sellable, obsolete])
         (product_product_4c, [product_product_4g product_product_4f])
        """
        # Create a purchase order with two lines.
        order = self.create_po()
        sellable_product = self.product_obj.browse(self.sellable_product)
        draft_product = self.product_obj.browse(self.draft_product)
        self.create_pol(order, sellable_product)
        self.create_pol(order, draft_product)
        self.assertNotIn('obsolete',
                         order.order_line.mapped('product_id.state2'))

        # Update sellable product to obsolete
        # NOTE: This check check the write() method of the product.product
        # record.
        self.assertIn(sellable_product, order.order_line.mapped('product_id'))
        self.assertEqual(sellable_product.state2, 'sellable')
        sellable_product.state2 = 'obsolete'
        self.assertEqual(sellable_product.state2, 'obsolete')

        # Check that the purchase order line now have a obsolete line.
        obsolete_order_line = order.order_line.filtered(
            lambda line: line.product_id.state2 == 'obsolete')
        self.assertTrue(obsolete_order_line)
        self.assertEqual(obsolete_order_line.product_id, sellable_product)

        # Simulate click on the "Check Discontinued Products" button to run the
        # replacemenet product wizard.
        wiz = self.wiz_obj.with_context({
            'active_id': order.id,
            'active_ids': [order.id],
            'active_model': 'purchase.order',
        }).create({})

        # Chech that the wizard auto create correctly the replacement lines.
        # The replacement line must be linked/generate to the obsolete purchase
        # order line.
        self.assertTrue(wiz.lines)
        self.assertEqual(len(wiz.lines), 1)
        self.assertEqual(obsolete_order_line, wiz.lines.mapped('line_id'))

        # TODO add a case to try to add a new replacement line manually. this
        # must be fail.

        # Try to add an obsolete replacement product in the replacement line.
        # This will raise an exception becuase only not obsolete products can
        # be used as a valid replacement.
        wiz_line = wiz.lines[0]
        with self.assertRaises(exceptions.ValidationError):
            wiz_line.replacement_product_id = self.obsolete_replacement

        # Add a sellable replacement product in the replacement line.
        wiz_line.replacement_product_id = self.sellable_replacement
        self.assertEqual(wiz_line.replacement_product_id.id,
                         self.sellable_replacement)

        # Make the replacement in the purchase order by clicking the button
        # "Replace" in the replacement wizard and check that the changes were
        # applied to the purchase order line.
        wiz.replacement()
        self.assertEqual(obsolete_order_line.product_id,
                         wiz_line.replacement_product_id)
        self.assertEqual(obsolete_order_line.discontinued_product_id,
                         wiz_line.discontinued_product_id)
