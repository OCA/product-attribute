# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class ProductCase(TransactionCase):
    def setUp(self):
        super(ProductCase, self).setUp()
        Product = self.env["product.product"]
        self.included = (
            Product.create({
                "name": "Included 1",
                "type": "product",
                "list_price": 100,
            }) |
            Product.create({
                "name": "Included 2",
                "type": "product",
                "list_price": 200,
            })
        )
        for product in self.included:
            chqtywiz = self.env["stock.change.product.qty"].create({
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "new_quantity": 10,
            })
            chqtywiz.change_product_qty()
        self.bundle = Product.create({
            "name": "Bundle",
            "list_price": 250,
            "bundle_ok": True,
            "bundle_line_ids": [
                (0, 0, {
                    "qty": 1,
                    "product_id": self.included[0].id,
                }),
                (0, 0, {
                    "qty": 3,
                    "product_id": self.included[1].id,
                }),
            ],
        })

    def test_total_price(self):
        """Total price computation is OK."""
        amount = 0
        for line in self.bundle.bundle_line_ids:
            self.assertEqual(
                line.total_lst_price,
                line.qty * line.product_id.lst_price)
            amount += line.total_lst_price
        self.assertEqual(self.bundle.bundle_lines_lst_price, amount)

    def test_no_change_company(self):
        """Cannot bundle products from other companies."""
        newcompany = self.env["res.company"].create({
            "name": "New company",
        })
        with self.assertRaises(ValidationError):
            with self.cr.savepoint():
                self.bundle.company_id = newcompany
        with self.assertRaises(ValidationError):
            with self.cr.savepoint():
                self.included[0].company_id = newcompany

    # TODO Remove if we actually implement this
    def test_no_variants(self):
        """Bundles have no variants."""
        attribute = self.env["product.attribute"].create({
            "name": "Some attr",
        })
        with self.assertRaises(ValidationError):
            self.bundle.product_tmpl_id.attribute_line_ids = [
                (0, 0, {
                    "attribute_id": attribute.id,
                })
            ]

    def test_only_consu(self):
        """Bundles are always consumable."""
        self.assertEqual(self.bundle.type, "consu")
        with self.assertRaises(ValidationError):
            self.bundle.type = "product"
        with self.assertRaises(ValidationError):
            self.bundle.type = "service"

    def test_bundle_delete_variants(self):
        """Onchange deletes product attributes when it is marked as bundle."""
        attribute = self.env["product.attribute"].create({
            "name": "Some attr",
        })
        tpl = self.included[0].product_tmpl_id
        with self.env.do_in_onchange():
            tpl.attribute_line_ids = [
                (0, 0, {
                    "attribute_id": attribute.id,
                })
            ]
            tpl.bundle_ok = True
            tpl._onchange_bundle_delete_variants()
            self.assertFalse(tpl.attribute_line_ids)

    def test_write_bundle_lines(self):
        """Ensure you can actually write lines to a bundle."""
        tpl = self.bundle.product_tmpl_id
        prod = self.included[0].copy()
        tpl.bundle_line_ids = [
            (5, 0, 0),
            (0, 0, {
                "qty": 1,
                "product_id": prod.id,
            })
        ]

    def test_stock(self):
        """Bundle stock is cumputed OK."""
        for product in (self.bundle, self.bundle.product_tmpl_id):
            # TODO Test also "outgoing_qty" and "incoming_qty"
            for qty in ("qty_available", "virtual_available"):
                _logger.debug(
                    "%s of %s should be 3...", qty, product)
                self.assertEqual(product[qty], 3)
                _logger.debug("... good, it was!")
