# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestModule(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env.ref("product_pricelist_margin.demo_product")
        self.wizard = (
            self.env["wizard.preview.pricelist.margin"]
            .with_context(active_model="product.product", active_id=self.product.id)
            .create({})
        )

    def _get_wizard_line(self, pricelist_xml_id):
        for line in self.wizard.line_ids:
            if line.pricelist_id == self.env.ref(pricelist_xml_id):
                return line
        return False

    def test_buttons(self):
        self.product.button_margin_per_pricelist()
        self.product.product_tmpl_id.button_margin_per_pricelist()

    def test_margin_computation(self):
        line = self._get_wizard_line("product.list0")
        self.assertEquals(
            line.margin_percent,
            50.0,
            "By default a product with a cost of 20 and a sale price of 40"
            " should have a margin of 50%.",
        )

        self.assertEquals(
            line.bg_color,
            "rgb(105, {green:.0f}, {blue:.0f})".format(
                green=105 + 1.5 * 50, blue=255 - 1.5 * 50
            ),
        )

        # We set a date when the pricelist has an exception
        self.wizard.price_date = "2000-01-02"
        line = self._get_wizard_line("product.list0")
        self.assertEquals(line.margin_percent, 75.0)
