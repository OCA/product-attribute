# Copyright 2026 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.product.tests.common import ProductCommon


class ProductSetCommon(ProductCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner_1 = cls.env["res.partner"].create({"name": "Test Partner One"})
        cls.partner_2 = cls.env["res.partner"].create({"name": "Test Partner Two"})
        cls.uom_1 = cls.env.ref("uom.product_uom_unit")
        cls.product_uom_1 = cls.env["product.uom"].create(
            {
                "barcode": "Test UoM 1",
                "uom_id": cls.uom_1.id,
                "product_id": cls.product.id,
            }
        )
        cls.product_set_1 = cls._create_product_set(
            "i5 computer offer",
            set_lines=[
                {
                    "product_id": cls.product.id,
                    "quantity": 1,
                    "product_uom_id": cls.product_uom_1.id,
                }
            ],
        )
        cls.product_set_2 = cls._create_product_set(
            "Services",
            set_lines=[{"product_id": cls.product.id, "quantity": 1}],
        )

        cls.product_set_line_1 = cls.product_set_1.set_line_ids[0]

    @classmethod
    def _create_product_set(cls, name, set_lines=None, **values):
        vals = {"name": name, **values}
        if set_lines:
            vals["set_line_ids"] = [
                Command.create(line_vals) for line_vals in set_lines
            ]
        return cls.env["product.set"].create(vals)
