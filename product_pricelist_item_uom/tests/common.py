# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.api import SUPERUSER_ID
from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestPricelistItemUomCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_pack_6 = cls.env.ref("uom.product_uom_pack_6")

        cls.product_tmpl = cls.env["product.template"].create(
            {
                "name": "Test Packaging Product",
                "list_price": 100.0,
                "uom_id": cls.uom_unit.id,
                "uom_ids": [Command.link(cls.uom_pack_6.id)],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Test Packaging Pricelist"}
        )
        cls.product_category = cls.env["product.category"].create(
            {"name": "Test Packaging Category"}
        )
        cls._enable_uom_feature()

    @classmethod
    def _enable_uom_feature(cls):
        """Turn on the "Units of Measure & Packagings" feature.

        ``_has_multiple_uoms`` reports the feature as enabled only when the
        root user belongs to the group, hence the direct membership.
        """
        cls.env.ref("uom.group_uom").sudo().user_ids |= cls.env["res.users"].browse(
            SUPERUSER_ID
        )

    @classmethod
    def _create_rule(cls, **values):
        return cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_tmpl.id,
                "compute_price": "fixed",
                **values,
            }
        )
