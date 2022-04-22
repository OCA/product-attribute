# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import exceptions

from .common import CommonCase


class TestCompanyCase(CommonCase):
    def test_create_default(self):
        rec = self.env["res.company"].create({"name": "ACME Inc."})
        self.assertEqual(
            rec.default_product_allowed_config_id.name,
            "Default product allowed configuration: ACME Inc.",
        )

    def test_create(self):
        rec = self.env["res.company"].create(
            {
                "name": "ACME Inc.",
                "default_product_allowed_config_id": self.product_list.id,
            }
        )
        self.assertEqual(rec.default_product_allowed_config_id, self.product_list)

    def test_write(self):
        rec = self.env.ref("base.main_company")
        rec.default_product_allowed_config_id = self.product_list
        with self.assertRaisesRegex(
            exceptions.ValidationError,
            "Default product allowed configuration is required",
        ):
            rec.default_product_allowed_config_id = False
