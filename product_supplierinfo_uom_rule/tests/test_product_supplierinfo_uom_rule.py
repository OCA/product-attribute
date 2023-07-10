# Copyright 2019- WT-IO-IT GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('-at_install', 'post_install', 'supplierinfo')
class TestProductSupplierinfoUomRule(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductSupplierinfoUomRule, cls).setUpClass()
        cls.vendor = cls.env['res.partner'].create({
            'name': 'Suplier with different UoM Price Rule',
            'supplier': True,
        })
        cls.product1 = cls.env['product.template'].create({
            'name': 'Product'
        })
        cls.supplierinfo = cls.env['product.supplierinfo'].create({
            'name': cls.vendor.id,
            'product_tmpl_id': cls.product1.id,
            'price': 100.0,
        })

    def test_product_supplierinfo_uom_rule_price_onchange(self):

        # Make sure that the rule price is correctly computed and
        # the original price stays unchanged
        dozen = self.env.ref('uom.product_uom_dozen')
        self.supplierinfo.rule_uom_id = dozen

        self.supplierinfo.onchange_rule_qty_uom()
        self.assertAlmostEqual(self.supplierinfo.rule_price, 1200.0)
        self.assertAlmostEqual(self.supplierinfo.price, 100.0)

        # Make sure the change of UoM Category will trigger a user error
        gram = self.env.ref('uom.product_uom_gram')

        self.supplierinfo.rule_uom_id = gram
        with self.assertRaises(UserError):
            self.supplierinfo.onchange_rule_qty_uom()
