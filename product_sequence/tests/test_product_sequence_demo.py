# Copyright 2026 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged
from odoo.tools.convert import convert_file


@tagged("post_install", "-at_install")
class TestProductSequenceDemo(TransactionCase):
    """The demo data must illustrate every way a reference is assigned.

    Since 19.0 Odoo does not load demo data by default, so the demo files are
    loaded here when they are missing. That way the demo data keeps being
    checked whether or not the database was created with demo data.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.env.ref(
            "product_sequence.product_template_demo_floor_lamp",
            raise_if_not_found=False,
        ):
            for filename in (
                "demo/res_company_demo.xml",
                "demo/product_category_demo.xml",
                "demo/product_template_demo.xml",
            ):
                convert_file(
                    cls.env,
                    "product_sequence",
                    filename,
                    None,
                    mode="init",
                    noupdate=True,
                )

    def _demo_ref(self, xmlid):
        return self.env.ref(f"product_sequence.{xmlid}").default_code

    def test_demo_category_prefix(self):
        """A category prefix drives the reference of its products."""
        self.assertRegex(self._demo_ref("product_template_demo_floor_lamp"), r"^LAMP")
        self.assertRegex(self._demo_ref("product_template_demo_office_chair"), r"^FURN")

    def test_demo_parent_category_prefix(self):
        """A category without prefix falls back on its parent prefix."""
        self.assertFalse(
            self.env.ref(
                "product_sequence.product_category_demo_desk_lamps"
            ).code_prefix
        )
        self.assertRegex(self._demo_ref("product_template_demo_desk_lamp"), r"^LAMP")

    def test_demo_default_sequence(self):
        """A product without category falls back on the default sequence."""
        self.assertRegex(
            self._demo_ref("product_template_demo_extension_cord"), r"^PR/"
        )
