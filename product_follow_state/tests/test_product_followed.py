# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestProductFollowed(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmpl_obj = cls.env["product.template"]
        cls.prod_obj = cls.env["product.product"]
        # Create product access for a non system user
        vals = {
            "name": "Group Test",
        }
        cls.group = cls.env["res.groups"].create(vals)
        vals = {
            "name": "Product Template Manager",
            "model_id": cls.env.ref("product.model_product_template").id,
            "group_id": cls.group.id,
            "perm_read": True,
            "perm_create": True,
            "perm_write": True,
            "perm_unlink": True,
        }
        cls.env["ir.model.access"].create(vals)
        vals = {
            "name": "Product Product Manager",
            "model_id": cls.env.ref("product.model_product_product").id,
            "group_id": cls.group.id,
            "perm_read": True,
            "perm_create": True,
            "perm_write": True,
            "perm_unlink": True,
        }
        cls.env["ir.model.access"].create(vals)

        cls.company_1 = cls.env.ref("base.main_company")
        vals = {
            "name": "Company 2",
        }
        cls.company_2 = cls.env["res.company"].create(vals)
        cls.user_demo = cls.env.ref("base.user_demo")

    def test_product_followed(self):
        """
        Set product not_followed on product in Company 1
        Change user to company 2
        not_followed value should be False
        """

        self.user_demo.write(
            {
                "groups_id": [(4, self.group.id)],
                "company_id": self.company_1.id,
                "company_ids": [(6, 0, [self.company_1.id, self.company_2.id])],
            }
        )

        prd = self.prod_obj.create(
            {
                "name": "Tests NewPrd",
                "company_id": self.company_1.id,
                "type": "consu",
            }
        )

        prd_usr = self.prod_obj.with_user(self.user_demo).browse(prd.id)
        self.assertTrue(prd_usr.followed)
        prods = self.prod_obj.with_user(self.user_demo).search(
            [("followed", "=", True)]
        )
        self.assertIn(prd_usr.id, prods.ids)
        prd_usr.not_followed = True
        self.assertFalse(prd_usr.followed)
        prods = self.prod_obj.with_user(self.user_demo).search(
            [("followed", "=", False)]
        )
        self.assertEqual(prods.id, prd_usr.id)

        # Switch company on User
        self.user_demo.write(
            {
                "company_id": self.company_2.id,
            }
        )
        prd_usr.invalidate_cache()
        prd_usr = self.prod_obj.with_user(self.user_demo).browse(prd.id)
        self.assertFalse(prd_usr.not_followed)
        self.assertTrue(prd_usr.followed)
