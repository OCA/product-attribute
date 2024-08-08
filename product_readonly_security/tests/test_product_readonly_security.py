# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user
from odoo.tests.common import users
from odoo.tools import mute_logger


class TestProductReadonlySecurity(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
                test_product_readonly_security=True,
            )
        )
        cls.user_admin = new_test_user(
            cls.env,
            login="test_user_admin",
            groups="base.group_user,base.group_system,%s"
            % ("product_readonly_security.group_product_edition"),
        )
        cls.user_readonly = new_test_user(
            cls.env,
            login="test_user_readonly",
            groups="base.group_user,base.group_system",
        )
        cls.product_tmpl = (
            cls.env["product.template"].sudo().create({"name": "Test product"})
        )
        cls.product = cls.product_tmpl.product_variant_ids

    @users("test_user_admin")
    @mute_logger("odoo.models.unlink")
    def test_product_template_admin(self):
        """Read, write, unlink and create allowed."""
        product_tmpls = self.env["product.template"].search([])
        self.assertIn(self.product_tmpl, product_tmpls)
        self.product_tmpl.with_user(self.env.user).write({"name": "new-name"})
        self.product_tmpl.with_user(self.env.user).unlink()
        new_product_tmpl = self.env["product.template"].create(
            {"name": "Test product 2"}
        )
        self.assertTrue(new_product_tmpl.exists())

    @users("test_user_readonly")
    def test_product_template_readonly(self):
        """Read allowed. Write, unlink and create not allowed."""
        product_tmpls = self.env["product.template"].search([])
        self.assertIn(self.product_tmpl, product_tmpls)
        with self.assertRaises(AccessError):
            self.product_tmpl.with_user(self.env.user).write({"name": "new-name"})
        with self.assertRaises(AccessError):
            self.product_tmpl.with_user(self.env.user).unlink()
        with self.assertRaises(AccessError):
            self.env["product.template"].create({"name": "Test product 2"})

    @users("test_user_admin")
    @mute_logger("odoo.models.unlink")
    def test_product_product_admin(self):
        """Read, write, unlink and create allowed."""
        products = self.env["product.product"].search([])
        self.assertIn(self.product, products)
        self.product.with_user(self.env.user).write({"name": "new-name"})
        self.product.with_user(self.env.user).unlink()
        new_product = self.env["product.product"].create({"name": "Test product 2"})
        self.assertTrue(new_product.exists())

    @users("test_user_readonly")
    def test_product_product_readonly(self):
        """Read allowed. Write, unlink and create not allowed."""
        products = self.env["product.product"].search([])
        self.assertIn(self.product, products)
        with self.assertRaises(AccessError):
            self.product.with_user(self.env.user).write({"name": "new-name"})
        with self.assertRaises(AccessError):
            self.product.with_user(self.env.user).unlink()
        with self.assertRaises(AccessError):
            self.env["product.product"].create({"name": "Test product 2"})
