# Copyright 2026 360ERP (https://www.360erp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestFieldlessWrite(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Avoid touching stock.move (and its access rights) when standard_price
        # is changed, just like product_cost_security's own tests do.
        cls.env = cls.env(context=dict(cls.env.context, disable_auto_svl=True))
        # base.group_system is the only group in the dependency graph that
        # grants CRUD access to products, so we use it to give edit rights on
        # products themselves (separate from the cost-edit permission).
        cls.reader = new_test_user(
            cls.env,
            "fieldless_reader",
            groups="base.group_system,product_cost_security.group_product_cost",
        )
        cls.editor = new_test_user(
            cls.env,
            "fieldless_editor",
            groups="base.group_system,product_cost_security.group_product_edit_cost",
        )
        cls.template = cls.env["product.template"].create({"name": "Test Product"})

    def test_empty_write_without_edit_group(self):
        """A field-less write must not be denied to a non cost-editor.

        This is the regression: an empty ``vals`` dict makes the ORM expand the
        checked fields to *all* accessible fields (including the protected cost
        fields), which used to wrongly raise an ``AccessError``.
        """
        template = self.template.with_user(self.reader)
        try:
            template.write({})
            template.write({"name": "Renamed Product"})
        except AccessError as error:
            self.fail(
                "A field-less write was wrongly denied to a non cost-editor: "
                f"{error}"
            )

    def test_delegated_write_without_edit_group(self):
        """Writing only fields another module pops off ``vals`` must succeed.

        ``l10n_eu_product_adr`` pops ``is_dangerous``/``adr_goods_id`` and
        delegates an empty dict to ``super().write({})``. Only run this when
        that module is installed and contributes the field.
        """
        if "is_dangerous" not in self.env["product.template"]._fields:
            self.skipTest("l10n_eu_product_adr is not installed")
        template = self.template.with_user(self.reader)
        template.write({"is_dangerous": True})
        self.assertTrue(template.is_dangerous)

    def test_cost_field_still_protected_without_edit_group(self):
        """The cost-edit restriction must still block a non cost-editor."""
        template = self.template.with_user(self.reader)
        with self.assertRaises(AccessError):
            template.write({"standard_price": 99.0})

    def test_cost_field_write_with_edit_group(self):
        """A cost-editor can still update the protected cost field."""
        template = self.template.with_user(self.editor)
        template.write({"standard_price": 42.0})
        self.assertEqual(template.standard_price, 42.0)
