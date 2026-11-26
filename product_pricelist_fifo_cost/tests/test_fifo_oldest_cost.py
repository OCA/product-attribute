# Copyright 2026 Marcos Mendez <m@pop.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestFifoOldestCost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.category = cls.env["product.category"].create(
            {"name": "Parts", "property_cost_method": "fifo"}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Part",
                "is_storable": True,
                "categ_id": cls.category.id,
                "standard_price": 7.0,
            }
        )
        cls.stock = cls.env.ref("stock.stock_location_stock")
        cls.supplier = cls.env.ref("stock.stock_location_suppliers")
        cls.customer = cls.env.ref("stock.stock_location_customers")
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "FIFO cost + 50%",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "fifo_oldest_cost",
                            "price_markup": 50.0,
                        },
                    )
                ],
            }
        )

    def _move(self, qty, src, dest, price=0.0):
        move = self.env["stock.move"].create(
            {
                "name": "move",
                "product_id": self.product.id,
                "product_uom_qty": qty,
                "product_uom": self.product.uom_id.id,
                "location_id": src.id,
                "location_dest_id": dest.id,
                "price_unit": price,
            }
        )
        move._action_confirm()
        move._action_assign()
        move.quantity = qty
        move.picked = True
        move._action_done()
        return move

    def _price(self, product=None, uom=None):
        return self.pricelist._get_product_price(
            product or self.product, 1.0, uom=uom or self.product.uom_id
        )

    def test_oldest_lot_sets_the_price(self):
        self._move(20, self.supplier, self.stock, 10.0)
        self._move(20, self.supplier, self.stock, 15.0)
        # The core cost is the average of the stock; the rule keeps the oldest.
        self.assertAlmostEqual(self.product.standard_price, 12.5)
        self.assertAlmostEqual(self._price(), 15.0)
        self._move(10, self.stock, self.customer)
        self.assertAlmostEqual(self._price(), 15.0)
        self._move(10, self.stock, self.customer)
        self.assertAlmostEqual(self._price(), 22.5)

    def test_template_and_uom(self):
        self._move(5, self.supplier, self.stock, 4.0)
        self.assertAlmostEqual(self._price(product=self.product.product_tmpl_id), 6.0)
        dozen = self.env.ref("uom.product_uom_dozen")
        self.assertAlmostEqual(self._price(uom=dozen), 72.0)

    def test_without_stock_uses_cost(self):
        self.assertAlmostEqual(self._price(), 10.5)
        dozen = self.env.ref("uom.product_uom_dozen")
        self.assertAlmostEqual(self._price(uom=dozen), 126.0)

    def test_labels_and_other_bases(self):
        rule = self.pricelist.item_ids
        self.assertIn("FIFO cost of the oldest lot", rule.price)
        rule.write({"base": "list_price", "price_markup": 0.0})
        self.assertIn("sales price", rule.price)
        self.product.list_price = 99.0
        self.assertAlmostEqual(self._price(), 99.0)
