# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super().setUp()
        self.template = self.env.ref(
            "product.product_product_4_product_template")
        self.all_variants = self.template.mapped("product_variant_ids")

    def test_product_2_template(self):
        count = 0
        # Disable all variant except one
        for variant in self.all_variants[:-1]:
            count += 1
            variant.active = False
            self.assertEqual(
                self.template.active, True,
                "Disabling %d of the %d variants should not disable"
                " the template." % (count, len(self.all_variants)))

        # Disable the last variant
        self.all_variants[-1:].active = False
        self.assertEqual(
            self.template.active, False,
            "Disabling all variants should disable the template.")

        # Enable again the last variant
        self.all_variants[-1:].active = True
        self.assertEqual(
            self.template.active, True,
            "Enable a variant should enable the template.")

    def test_template_2_product(self):
        """non-regression testing"""

        self.template.active = False
        self.assertEqual(
            any(self.all_variants.mapped("active")), False,
            "Disable a template should disable all the variants.")

        self.template.active = True
        self.assertEqual(
            all(self.all_variants.mapped("active")), True,
            "Enable a template should enable all the variants.")
