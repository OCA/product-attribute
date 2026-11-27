# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import exceptions

from .common import CommonCase


class TestCompanyCase(CommonCase):
    def test_create_default(self):
        rec = self.env["res.company"].create({"name": "ACME Inc."})
        self.assertEqual(
            rec.default_seasonal_config_id.name,
            "Default product seasonal configuration: ACME Inc.",
        )

    def test_create(self):
        rec = self.env["res.company"].create(
            {"name": "ACME Inc.", "default_seasonal_config_id": self.seasonal_conf.id}
        )
        self.assertEqual(rec.default_seasonal_config_id, self.seasonal_conf)

    def test_write(self):
        rec = self.env.ref("base.main_company")
        rec.default_seasonal_config_id = self.seasonal_conf
        with self.assertRaisesRegex(
            exceptions.ValidationError,
            "Default product seasonal configuration is required",
        ):
            rec.default_seasonal_config_id = False
