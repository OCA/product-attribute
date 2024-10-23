# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class Tests(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductTemplate = cls.env["product.template"]
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.category_normal = cls.env.ref("product.product_category_all")
        cls.category_special = cls.env.ref(
            "product_category_usage_group.category_usage_group"
        )
        cls.product_group = cls.env.ref("base.group_system")
        cls.restricted_group = cls.env.ref("base.group_multi_company")
        # Set only Root user as member of the restricted group
        cls.restricted_group.users = False
        cls.restricted_group.users += cls.user_admin
        # Allow demo user to create template
        cls.product_group.users += cls.user_demo

    def test_01_access_user_without_right(self):
        # Use a category without restricted access should success
        self._create_product(self.user_demo, self.category_normal)
        # Use a category with restricted access should fail
        with self.assertRaises(ValidationError):
            self._create_product(self.user_demo, self.category_special)

    def test_02_access_user_with_right(self):
        # Use a category without restricted access should success
        self._create_product(self.user_admin, self.category_normal)
        # Use a category with restricted access should success
        self._create_product(self.user_admin, self.category_special)

    def _create_product(self, user, category):
        self.ProductTemplate.with_user(user).create(
            {"name": "Demo Product", "categ_id": category.id}
        )
