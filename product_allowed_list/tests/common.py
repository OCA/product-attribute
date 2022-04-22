# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class CommonCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_list = cls.env["product.allowed.list"].create(
            {"name": "Test product list conf"}
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
                "product_template_id": cls.prod1.product_tmpl_id.id,
                "product_id": cls.prod1.id,
            },
            {
                "product_template_id": cls.prod2.product_tmpl_id.id,
            },
        ]
        write_values = []
        for vals in line_values:
            vals["product_allowed_list_id"] = cls.product_list.id
            write_values.append((0, 0, vals))
        cls.product_list.write({"line_ids": write_values})
