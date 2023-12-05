#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from math import log10

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestProductPricelistItem(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.g_uom = cls.env.ref("uom.product_uom_gram")
        cls.kg_uom = cls.env.ref("uom.product_uom_kgm")

        # Converting g to kg needs to increase accuracy
        cls.uom_accuracy = cls.env.ref("product.decimal_product_uom")
        cls.uom_accuracy.digits = log10(cls.g_uom.factor)

        # UoM group needed to see UoM field
        cls.env.user.groups_id += cls.env.ref("uom.group_uom")
        product_1000_kg_form = Form(cls.env["product.product"])
        product_1000_kg_form.name = "Test product"
        product_1000_kg_form.uom_id = cls.kg_uom
        product_1000_kg_form.lst_price = 1000
        cls.product_1000_kg = product_1000_kg_form.save()

        # Activate advanced pricelist to apply surcharge
        cls.env.user.groups_id += cls.env.ref("product.group_sale_pricelist")
        pricelist_g_kg_form = Form(cls.env["product.pricelist"])
        pricelist_g_kg_form.name = "Test pricelist"
        with pricelist_g_kg_form.item_ids.new() as item:
            item.applied_on = "0_product_variant"
            item.product_id = cls.product_1000_kg
            item.compute_price = "formula"
            item.price_surcharge = 500
            item.uom_id = cls.g_uom
            item.uom_min_quantity = 1
        with pricelist_g_kg_form.item_ids.new() as item:
            item.applied_on = "0_product_variant"
            item.product_id = cls.product_1000_kg
            item.compute_price = "formula"
            item.uom_id = cls.kg_uom
            item.uom_min_quantity = 1
        cls.pricelist_g_kg = pricelist_g_kg_form.save()

    def test_sync_uom_min_quantity(self):
        g_uom = self.g_uom
        kg_uom = self.kg_uom
        pricelist = self.pricelist_g_kg
        pricelist_form = Form(pricelist)
        with pricelist_form.item_ids.edit(0) as item:
            self.assertEqual(item.uom_id, kg_uom)
            self.assertEqual(item.min_quantity, 1)
            self.assertEqual(item.uom_min_quantity, 1)

            item.uom_id = g_uom
            self.assertEqual(item.min_quantity, 0.001)
            self.assertEqual(item.uom_min_quantity, 1)

            item.min_quantity = 1
            self.assertEqual(item.uom_min_quantity, 1000)

            item.uom_min_quantity = 1
            self.assertEqual(item.min_quantity, 0.001)

    def test_product_price(self):
        g_uom = self.g_uom
        kg_uom = self.kg_uom
        product = self.product_1000_kg
        pricelist = self.pricelist_g_kg

        g_price, g_rule = pricelist._compute_price_rule(
            product,
            1,
            uom=g_uom,
        )[product.id]
        kg_price, kg_rule = pricelist._compute_price_rule(
            product,
            1,
            uom=kg_uom,
        )[product.id]

        self.assertEqual(g_price, 1.5)
        self.assertEqual(kg_price, 1000)
