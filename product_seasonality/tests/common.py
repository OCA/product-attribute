# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.product_allowed_list.tests.common import CommonCase


class CommonCaseWithSeasonalLines(CommonCase):
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
        write_values = [(5, 0)]
        for vals in line_values:
            vals["product_allowed_list_id"] = cls.product_list.id
            write_values.append((0, 0, vals))
        cls.product_list.write({"line_ids": write_values})
