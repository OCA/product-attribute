# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command
from odoo.tests import common, tagged

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@tagged("post_install", "-at_install")
class CommonProductPricelistAlternative(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env["base"].with_context(**DISABLED_MAIL_CONTEXT).env
        cls.datacard = cls.env["product.product"].create(
            {"name": "Data card", "list_price": 100}
        )
        cls.usb_adapter = cls.env["product.product"].create(
            {"name": "Usb adapter", "list_price": 100}
        )

        cls.alternative_pricelist_01 = cls.env["product.pricelist"].create(
            {
                "name": "Alternative pricelist 01",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.usb_adapter.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                ],
            }
        )
        cls.alternative_pricelist_02 = cls.env["product.pricelist"].create(
            {
                "name": "Alternative pricelist 02",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.datacard.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 80,
                        }
                    ),
                ],
            }
        )

        cls.pricelist01 = cls.env["product.pricelist"].create(
            {
                "name": "Sale pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.usb_adapter.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 95,
                        }
                    ),
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": cls.datacard.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 70,
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    (4, cls.alternative_pricelist_01.id),
                    (4, cls.alternative_pricelist_02.id),
                ],
            }
        )

        cls.product_categ01 = cls.env["product.category"].create(
            {"name": "Category 01"}
        )
        cls.usb_adapter.categ_id = cls.product_categ01

        cls.pricelist02 = cls.env["product.pricelist"].create(
            {
                "name": "Sale pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "percentage",
                            "applied_on": "2_product_category",
                            "categ_id": cls.product_categ01.id,
                            "percent_price": 40,
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    (4, cls.alternative_pricelist_01.id),
                ],
            }
        )
