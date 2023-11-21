#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command, first
from odoo.tests import TransactionCase


class TestPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        pricelist_model = cls.env["product.pricelist"]
        cls.base_pricelist = pricelist_model.create(
            {
                "name": "Base",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "percentage",
                            "percent_price": 10,
                            "applied_on": "3_global",
                        }
                    ),
                ],
            }
        )
        cls.depending_pricelist = pricelist_model.create(
            {
                "name": "Depending",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.base_pricelist.id,
                            "price_discount": 10,
                            "applied_on": "3_global",
                        }
                    ),
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.base_pricelist.id,
                            "price_discount": 10,
                            "applied_on": "2_product_category",
                            "categ_id": cls.env.ref("product.product_category_all").id,
                        }
                    ),
                    Command.create(
                        {
                            "base": "list_price",
                            "compute_price": "formula",
                            "price_discount": 10,
                            "applied_on": "3_global",
                        }
                    ),
                ],
            }
        )

    def test_base_item_price_changed(self):
        """When changing the price of the base rule,
        only depending items/pricelists are updated."""
        # Arrange
        base_pricelist = self.base_pricelist
        base_item = base_pricelist.item_ids
        depending_pricelist = self.depending_pricelist
        depending_items = depending_pricelist.item_ids
        depending_item = first(
            depending_items.filtered(
                lambda item: item.base_pricelist_id == base_pricelist
                and item.applied_on == base_item.applied_on
            )
        )
        other_applied_item = first(
            depending_items.filtered(
                lambda item: item.base == depending_item.base
                and item.applied_on != depending_item.applied_on
            )
        )
        other_base_item = first(
            depending_items.filtered(
                lambda item: item.base != depending_item.base
                and item.applied_on == depending_item.applied_on
            )
        )
        # pre-condition
        self.assertFalse(depending_pricelist.is_base_price_changed)
        self.assertFalse(depending_item.is_base_price_changed)
        self.assertTrue(other_applied_item)
        self.assertTrue(other_base_item)
        self.assertFalse(other_applied_item.is_base_price_changed)
        self.assertFalse(other_base_item.is_base_price_changed)

        # Act
        base_item.percent_price = 20

        # Assert
        self.assertTrue(depending_pricelist.is_base_price_changed)
        self.assertTrue(depending_item.is_base_price_changed)
        self.assertFalse(other_applied_item.is_base_price_changed)
        self.assertFalse(other_base_item.is_base_price_changed)

    def test_uncheck_item_pricelist_changed(self):
        """When unchecking `is_base_price_changed` in the items,
        its pricelist is updated."""
        # Arrange
        base_pricelist = self.base_pricelist
        base_item = base_pricelist.item_ids
        base_item.percent_price = 20
        depending_pricelist = self.depending_pricelist
        depending_item = first(
            depending_pricelist.item_ids.filtered(
                lambda item: item.base_pricelist_id == base_pricelist
                and item.applied_on == base_item.applied_on
            )
        )
        # pre-condition
        self.assertTrue(depending_pricelist.is_base_price_changed)
        self.assertTrue(depending_item.is_base_price_changed)

        # Act
        depending_item.is_base_price_changed = False

        # Assert
        self.assertFalse(depending_pricelist.is_base_price_changed)
        self.assertFalse(depending_item.is_base_price_changed)
