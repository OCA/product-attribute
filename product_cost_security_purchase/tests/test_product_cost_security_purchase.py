# Copyright 2026 360ERP (<https://www.360erp.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import Command
from odoo.tests import Form, tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon

EXPRESSION_ATTRIBUTES = (
    "context",
    "domain",
    "invisible",
    "column_invisible",
    "readonly",
    "required",
)


@tagged("post_install", "-at_install")
class TestProductCostSecurityPurchase(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        groups = "base.group_user,purchase.group_purchase_manager"
        cls.user_no_cost = new_test_user(cls.env, login="no_cost", groups=groups)
        cls.user_cost = new_test_user(
            cls.env,
            login="cost",
            groups=f"{groups},product_cost_security.group_product_cost",
        )
        cls.template = cls.env["product.template"].create(
            {"name": "Test product", "standard_price": 12.5}
        )
        cls.vendor = cls.env["res.partner"].create({"name": "Vendor"})

    def _assert_no_cost_in_expressions(self, model):
        """The client must not have to evaluate a field it does not receive."""
        res = self.env[model].with_user(self.user_no_cost).get_views([(False, "form")])
        self.assertNotIn("standard_price", res["models"][model]["fields"])
        arch = etree.fromstring(res["views"]["form"]["arch"])
        for node in arch.iter(tag=etree.Element):
            for attribute in EXPRESSION_ATTRIBUTES:
                self.assertNotIn(
                    "standard_price",
                    node.get(attribute) or "",
                    f"{model}: <{node.tag} name={node.get('name')!r}> uses "
                    f"standard_price in {attribute!r}",
                )

    def test_template_form_without_cost_access(self):
        self._assert_no_cost_in_expressions("product.template")

    def test_variant_form_without_cost_access(self):
        self._assert_no_cost_in_expressions("product.product")

    def test_add_vendor_line_without_cost_access(self):
        form = Form(self.template.with_user(self.user_no_cost))
        with form.seller_ids.new() as line:
            line.partner_id = self.vendor
            self.assertEqual(line.price, 0.0)

    def test_add_vendor_line_with_cost_access(self):
        form = Form(self.template.with_user(self.user_cost))
        with form.seller_ids.new() as line:
            line.partner_id = self.vendor
            self.assertEqual(line.price, 12.5)

    def test_variant_default_price_uses_variant_cost(self):
        attribute = self.env["product.attribute"].create(
            {
                "name": "Size",
                "value_ids": [
                    Command.create({"name": "S"}),
                    Command.create({"name": "L"}),
                ],
            }
        )
        template = self.env["product.template"].create(
            {
                "name": "Product with variants",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [Command.set(attribute.value_ids.ids)],
                        }
                    )
                ],
            }
        )
        variant_s, variant_l = template.product_variant_ids
        variant_s.standard_price = 5.0
        variant_l.standard_price = 7.0
        supplierinfo = self.env["product.supplierinfo"].with_user(self.user_cost)
        defaults = supplierinfo.with_context(
            default_product_tmpl_id=template.id,
            product_cost_security_product_id=variant_l.id,
        ).default_get(["price"])
        self.assertEqual(defaults["price"], 7.0)
        defaults = (
            supplierinfo.with_user(self.user_no_cost)
            .with_context(
                default_product_tmpl_id=template.id,
                product_cost_security_product_id=variant_l.id,
            )
            .default_get(["price"])
        )
        self.assertEqual(defaults["price"], 0.0)

    def test_explicit_default_price_is_kept(self):
        defaults = (
            self.env["product.supplierinfo"]
            .with_user(self.user_cost)
            .with_context(default_product_tmpl_id=self.template.id, default_price=3.0)
            .default_get(["price"])
        )
        self.assertEqual(defaults["price"], 3.0)
