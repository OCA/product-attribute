# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# @author: Damien Crier <damien.crier@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .common import CommonCaseWithLines


class TestSeasonalityCase(CommonCaseWithLines):
    def test_display_name_with_variant(self):
        line = self.product_list.config_for_product(self.prod1)
        self.assertEqual(
            line.display_name,
            f"[{self.product_list.display_name}] {self.prod1.display_name} ({line.id})",
        )

    def test_display_name_with_template_only(self):
        line = self.product_list.config_for_product(self.prod1)
        line.product_id = False
        tmpl = line.product_template_id
        self.assertEqual(
            line.display_name,
            f"[{self.product_list.display_name}] {tmpl.display_name} ({line.id})",
        )
