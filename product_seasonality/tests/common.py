# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class CommonCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.seasonal_conf = cls.env["seasonal.config"].create(
            {"name": "Test seasonal conf"}
        )


class CommonCaseWithLines(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.prod1 = cls.env.ref("product.product_product_2")
        cls.prod2 = cls.env.ref("product.product_product_4")
        cls._setup_lines()

    @classmethod
    def _setup_lines(cls):
        line_values = [
            {
                "date_start": "2021-05-10",
                "date_end": "2021-05-16",
                "monday": True,
                "tuesday": True,
                "wednesday": True,
                "thursday": False,
                "friday": False,
                "saturday": False,
                "sunday": False,
                "product_template_id": cls.prod1.product_tmpl_id.id,
                "product_id": cls.prod1.id,
            },
            {
                "date_start": "2021-05-12",
                "date_end": "2021-05-23",
                "monday": False,
                "tuesday": False,
                "wednesday": False,
                "thursday": True,
                "friday": True,
                "saturday": True,
                "sunday": True,
                "product_template_id": cls.prod2.product_tmpl_id.id,
            },
        ]
        write_values = []
        for vals in line_values:
            vals["seasonal_config_id"] = cls.seasonal_conf.id
            write_values.append((0, 0, vals))
        cls.seasonal_conf.write({"line_ids": write_values})
