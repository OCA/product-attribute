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
from openerp.exceptions import ValidationError
import time


class TestProductLifecycle(common.TransactionCase):

    """
    - CRUD Tests over product.product
    - Purchase Order with obsolete lines.
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

          Product State           Replace By  Replace To
          A2323   In Development  A2327
          A2324   Obsolete        A2327
          A2325   Normal          A2329
    (new) A2327   End Of Life
    (new) A2328   Obsolete
    (new) A2329   Normal
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

        self.assertEqual(
            self.product_obj.browse(self.obsolete_replacement).state2,
            'obsolete')
        self.assertEqual(
            self.product_obj.browse(self.sellable_replacement).state2,
            'sellable')

    def create_product(self, w_replace_by=True):
        """ Create a new product """
        values = {
            "default_code": 'A2330',
            "product_tmpl_id":
            self.ref("product.product_product_4_product_template"),
            "attribute_value_ids": [(6, 0, [
                self.ref('product.product_attribute_value_1'),
                self.ref('product_lifecycle.product_attribute_value_6'),
                self.ref('product.product_attribute_value_5')])],
            }
        if w_replace_by:
            values.update({
                "replaced_by_product_id":
                self.ref('product_lifecycle.product_product_4e'),
            })
        product = self.product_obj.create(values)
        self.assertTrue(product)
        self.assertEqual(product.state2, 'draft')
        return product

    def create_pol(self, order, product):
        """
        Create a new purchase order line for the given purchase order taking
        as input only the product
        """
        write_flag = order.write({
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_qty': 10.0,
                'product_uom': product.uom_id.id,
                'price_unit': product.price,
                'name': product.name_template,
                'sequence': len(order.order_line) + 1,
                'date_planned': time.strftime('%Y-%m-%d')
            })]})
        self.assertTrue(write_flag)

    def create_po(self):
        """ Create a purchase order """
        pricelist_id = 1
        partner_id = self.ref('base.res_partner_1')
        order = self.order_obj.create({
            'partner_id': partner_id,
            'location_id': self.ref('stock.stock_location_stock'),
            'pricelist_id': pricelist_id})
        self.assertTrue(order)
        return order

    def replacement_wizard(self):
        """
        - Create a valid purchase order with multiple lines (not obsoletes)
        - Then update one of its line product to a obsolete product.
        - Check that the purchase order now have a obsolete line.
        - Simulate click on the "Replace Obsolete Products" button to run the
          replacement product wizard (Create a replacement wizard)
        - Check that the wizard auto create correctly the replacement lines
          (taking the obsolete line)

        :return: tuple (obsolete line, wiz, wiz_line)
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

        # Simulate click on "Replace Obsolete Products" button.
        wiz = self.wiz_obj.with_context({
            'active_id': order.id,
            'active_ids': [order.id],
            'active_model': 'purchase.order',
        }).create({})

        # Check that the wizard auto create correctly the replacement lines.
        # The replacement line must be linked/generate to the obsolete purchase
        # order line.
        self.assertTrue(wiz.lines)
        self.assertEqual(len(wiz.lines), 1)
        self.assertEqual(obsolete_order_line, wiz.lines.mapped('line_id'))

        return obsolete_order_line, wiz.lines[0]

    def test_01(self):
        """ Basic CRUD: Check create product, defaults and read.

        Create a new product and check it was correctly with the default
        product lifecycle state and the replacements products were link.
        """
        product = self.create_product(w_replace_by=False)
        self.assertTrue(product)
        self.assertEqual(product.state2, 'draft')

    def test_02(self):
        """ Basic CRUD: Check product write. Update product

        Update the product status. Get an already exist product and update its
        product lifecycle status from draft to sellable.
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

        # Update new product field (field defined outside this module)
        self.assertEqual(new_product.default_code, 'A2330')
        new_product.default_code = 'A2330-1'
        self.assertEqual(new_product.default_code, 'A2330-1')

        # Same but to an existing demo product.
        self.assertEqual(demo_product.default_code, 'A2329')
        demo_product.default_code = 'A2329-1'
        self.assertEqual(demo_product.default_code, 'A2329-1')

        # Update new product common characteristic (field defined in
        # product.template) and check that affects the another product
        # variants
        self.assertFalse(new_product.description)
        new_product.description = 'This is a New Product'
        self.assertEqual(new_product.description, 'This is a New Product')
        self.assertEqual(demo_product.description, 'This is a New Product')
        demo_product.description = False
        self.assertFalse(demo_product.description)

    def test_03(self):
        """ Basic CRUD: Delete product

        Now we are going to delete a recently created product record.
        """
        product = self.create_product()
        products = self.product_obj.search([])
        self.assertIn(product, products)
        product.unlink()
        self.assertNotIn(product.exists(), products)

    def test_04(self):
        """ Basic CRUD: Duplicate product. Use default state instead original.
        """
        new_product = self.product_obj.browse(self.obsolete_product).copy()
        self.assertTrue(new_product)
        self.assertEqual(new_product.state2, 'draft')

        # TODO Automatic purchase. Add one obsolete product line. This will be
        # added but replaced with the replacement product.

    def test_06(self):
        """ Replacement wizard: replace a obsolete line.

        This apply after create a purchase order one or more of its order line
        products change to obsolete state.

        This wizard take the obsolete order lines and replace with the
        replacement product defined at the product itself
        """
        obsolete_line, wiz_line = self.replacement_wizard()
        wiz_line.replacement_id.replacement()
        self.assertEqual(obsolete_line.product_id,
                         wiz_line.replace_product_id)

        # TODO add a case to try to add a new replacement line manually. This
        # must be fail.

    def test_07(self):
        """ Replacement wizard: try to replace with an obsolete product.

        Try to add an obsolete replacement product in the replacement line
        and try to make the replace. This will raise an exception because
        only not obsolete products can be used as a valid replacement.
        """
        _, wiz_line = self.replacement_wizard()
        msg_error = 'replace product can not be a obsolete product'
        with self.assertRaisesRegexp(ValidationError, msg_error):
            wiz_line.replace_product_id = self.obsolete_replacement

    def test_08(self):
        """ Replacement wizard: try to replace a sellable product

        Try to add an sellable obsolete product in the replacement line
        and try to make the replace. This will raise an exception because
        only obsolete products can be valid to replace.
        """
        _, wiz_line = self.replacement_wizard()
        msg_error = 'obsolete product must be a obsolete product'
        with self.assertRaisesRegexp(ValidationError, msg_error):
            wiz_line.obsolete_product_id = self.sellable_replacement

    def test_09(self):
        """ Constraint: Changing to obsolete with stock will change to End of
        life

        Trying to put a product to obsolete when have stock will change the
        product to end of life state instead.
        """
        # Create a new product without stock
        product = self.create_product()
        self.assertEqual(product.qty_available, 0.0)

        # Add product inventory by making a purchase and validating
        purchase_order = self.create_po()
        self.create_pol(purchase_order, product)
        purchase_order.signal_workflow('purchase_confirm')
        self.assertEqual(purchase_order.state, 'approved')
        purchase_order.picking_ids.do_transfer()
        self.assertGreater(product.qty_available, 0.0)

        # Try to set the product as obsolete but will not be able to do because
        # have stock. Instead will change to end state.

        # OLD API
        product.write({'state2': 'obsolete'})
        self.assertEqual(product.state2, 'end')

        # NEW API
        # TODO This next lines are failing, there is a cache problem check why.
        # product.state2 = 'obsolete'
        # self.assertEqual(product.state2, 'end')

    def test_10(self):
        """ Test method used in ir.cron to update product state.
            [On hand, incoming}
             1   00 = 0
             2   01 = 1
             3   10 = 1
             4   11 = 1
        """

        # Create a new product and change state to obsolete. This can be done
        # because the product is new and have not inventory.
        product = self.create_product()
        self.assertEqual(product.state2, 'draft')
        self.assertEqual(product.qty_available, 0.0)
        self.assertEqual(product.purchase_incoming_qty, 0.0)
        product.state2 = 'obsolete'
        self.assertEqual(product.state2, 'obsolete')

        # Then run the update product state method in this must remain obsolete
        product.update_product_state()
        self.assertEqual(product.state2, 'obsolete')

        # Purchase an obsolete product and confirm the purchase order will
        # update the product inventory values. There will be a incoming
        # quantity
        purchase_order = self.create_po()
        self.create_pol(purchase_order, product)
        purchase_order.signal_workflow('purchase_confirm')
        self.assertEqual(purchase_order.state, 'approved')
        self.assertEqual(product.qty_available, 0.0)
        self.assertEqual(product.purchase_incoming_qty, 10.0)

        # Then run the update product state method and must change to end state
        product.update_product_state()
        self.assertEqual(product.state2, 'end')

        # When confirm the picking of the purchase will make the products
        # available in quantity on hand. (100)
        purchase_order.picking_ids.do_transfer()
        self.assertEqual(product.qty_available, 10.0)
        self.assertEqual(product.purchase_incoming_qty, 0.0)

        # Then run the update product state method and remain in end state
        product.update_product_state()
        self.assertEqual(product.state2, 'end')

        # TODO 11 real + incoming > end # make another purchase
        # product.update_product_state()
        # self.assertEqual(product.state2, res.get('110'))
