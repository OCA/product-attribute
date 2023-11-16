# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class Common(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env["base"].with_context(**DISABLED_MAIL_CONTEXT).env
        cls.env.ref("stock.group_tracking_lot").users += cls.env.user
        cls.package_type_pallet = cls.env.ref("stock.package_type_01")
        cls.package_type_box = cls.env.ref("stock.package_type_02")
        cls.package_type_pallet.container_deposit_product_id = cls.env[
            "product.product"
        ].create(
            {
                "name": "EUROPAL",
                "detailed_type": "service",
            }
        )
        cls.package_type_box.container_deposit_product_id = cls.env[
            "product.product"
        ].create(
            {
                "name": "Box",
                "detailed_type": "service",
            }
        )
        cls.product_packaging_level_pallet = cls.env["product.packaging.level"].create(
            {
                "name": "PALLET",
                "code": "PAL",
                "sequence": 1,
                "name_policy": "by_package_type",
            }
        )
        cls.product_packaging_level_box = cls.env["product.packaging.level"].create(
            {
                "name": "BOX",
                "code": "BOX",
                "sequence": 1,
                "name_policy": "by_package_type",
            }
        )
        cls.packaging = cls.env["product.packaging"].create(
            [
                {
                    "name": "Box of 12",
                    "qty": 12,
                    "package_type_id": cls.package_type_box.id,
                    "packaging_level_id": cls.product_packaging_level_box.id,
                },
                {
                    "name": "Box of 24",
                    "qty": 24,
                    "package_type_id": cls.package_type_box.id,
                    "packaging_level_id": cls.product_packaging_level_box.id,
                },
                {
                    "name": "EU pallet",
                    "qty": 240,
                    "package_type_id": cls.package_type_pallet.id,
                    "packaging_level_id": cls.product_packaging_level_pallet.id,
                },
            ]
        )

        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "packaging_ids": [(6, 0, cls.packaging.ids)]}
        )

        # Copy packaging of product A to product B
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "Product B",
                "packaging_ids": [(6, 0, [pack.copy().id for pack in cls.packaging])],
            }
        )
        cls.product_c = cls.env["product.product"].create(
            {"name": "Product Test C (No packaging)"}
        )
        cls.pallet = cls.package_type_pallet.container_deposit_product_id
        cls.box = cls.package_type_box.container_deposit_product_id
