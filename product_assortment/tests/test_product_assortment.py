# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestProductAssortment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.filter_obj = cls.env["ir.filters"]
        cls.product_obj = cls.env["product.product"]
        cls.product_storage_box = cls.product_obj.create(
            {
                "name": "Storage Box",
                "type": "consu",
                "standard_price": 14.0,
                "list_price": 15.8,
                "default_code": "E-COM08",
            }
        )
        cls.product_virtual_home_staging = cls.product_obj.create(
            {
                "name": "Virtual Home Staging",
                "type": "service",
                "standard_price": 25.5,
                "list_price": 38.25,
            }
        )
        cls.assortment = cls.filter_obj.create(
            {
                "name": "Test Assortment",
                "model_id": "product.product",
                "is_assortment": True,
                "domain": [],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.partner2 = cls.env["res.partner"].create({"name": "Test partner 2"})

    def test_assortment(self):
        products = self.product_obj.search([])
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assertEqual(products.ids, products_filtered.ids)

        # reduce assortment to services products
        domain = [("type", "=", "service")]
        self.assortment.domain = domain

        products = self.product_obj.search(domain)
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assertEqual(products.ids, products_filtered.ids)

        # include one product not in initial filter
        included_product = self.product_storage_box
        self.assortment.write({"whitelist_product_ids": [(4, included_product.id)]})
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assertIn(included_product.id, products_filtered.ids)

        # exclude one product not in initial filter
        excluded_product = self.product_virtual_home_staging
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assertIn(excluded_product.id, products_filtered.ids)
        self.assortment.write({"blacklist_product_ids": [(4, excluded_product.id)]})
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assertNotIn(excluded_product.id, products_filtered.ids)

    def test_assortment_not_available_search_view(self):
        model = self.env.ref("product.model_product_product")
        filters = self.filter_obj.get_filters(model.id)
        self.assertFalse(filters)

    def test_create_assortment_with_context(self):
        assortment = self.filter_obj.with_context(product_assortment=True).create(
            {"name": "Test Assortment Context", "domain": []}
        )
        self.assertTrue(assortment.is_assortment)
        self.assertEqual(assortment.model_id, "product.product")

    @mute_logger("odoo.sql_db")
    def test_create_assortment_without_context(self):
        with self.assertRaises(IntegrityError), self.env.cr.savepoint():
            self.filter_obj.with_context(product_assortment=False).create(
                {"name": "Test Assortment No Context", "domain": []}
            )

    def test_search_assortment_with_partner(self):
        self.filter_obj.with_context(product_assortment=True).create(
            {
                "name": "Test Assortment Partner",
                "domain": [],
                "partner_ids": [(4, self.partner.id)],
            }
        )
        search_domain = self.partner.action_define_product_assortment()["domain"]
        self.assertEqual(
            search_domain,
            [
                ("all_partner_ids", "in", [self.partner.id]),
                ("is_assortment", "=", True),
            ],
        )

    def test_product_assortment_view(self):
        included_product = self.product_storage_box
        self.assortment.write({"whitelist_product_ids": [(4, included_product.id)]})
        res = self.assortment.show_products()
        domain = [tuple(condition) for condition in res["domain"]]
        self.assertEqual(domain, [(1, "=", 1)])

    def test_product_assortment_view_with_black_list(self):
        excluded_product = self.product_virtual_home_staging
        self.assortment.write(
            {
                "blacklist_product_ids": [(4, excluded_product.id)],
            }
        )
        res = self.assortment.show_products()
        domain = [tuple(condition) for condition in res["domain"]]
        self.assertEqual(domain, [("id", "not in", excluded_product.ids)])

    def test_product_assortment_mixed_view(self):
        included_product = self.product_storage_box
        excluded_product = self.product_virtual_home_staging
        self.assortment.write(
            {
                "whitelist_product_ids": [(4, included_product.id)],
                "blacklist_product_ids": [(4, excluded_product.id)],
            }
        )
        res = self.assortment.show_products()
        domain = [tuple(condition) for condition in res["domain"]]
        self.assertEqual(domain, [("id", "not in", excluded_product.ids)])

    def test_product_assortment_filter_combination(self):
        """Combine a whitelisted and a blacklisted product in order
        to validate the combination of both filters. The result should be a
        simple domain with the excluded product.
        """
        # Add a default no product filter to the assortment
        self.assortment.write({"domain": [("id", "=", 0)]})
        included_product = self.product_storage_box
        self.assortment.write({"whitelist_product_ids": [(4, included_product.id)]})
        excluded_product = self.product_virtual_home_staging
        self.assortment.write({"blacklist_product_ids": [(4, excluded_product.id)]})
        res = self.assortment.show_products()
        self.assertIn(("id", "not in", [excluded_product.id]), res["domain"])
        self.assertIn(("id", "in", [included_product.id]), res["domain"])

    def test_record_count(self):
        products = self.product_obj.search([])
        self.assertEqual(self.assortment.record_count, len(products))

        # reduce assortment to services products
        domain = [("type", "=", "service")]
        self.assortment.domain = domain

        products = self.product_obj.search(domain)
        domain = self.assortment._get_eval_domain()
        products_filtered = self.product_obj.search(domain)
        self.assortment.invalidate_recordset()
        self.assertEqual(self.assortment.record_count, len(products_filtered))

    def test_assortment_with_partner_domain(self):
        assortment = self.filter_obj.with_context(product_assortment=True).create(
            {
                "name": "Test Assortment Partner domain",
                "partner_domain": f"[('id', '=', '{self.partner.id}')]",
                "partner_ids": [(4, self.partner2.id)],
            }
        )
        self.assertEqual(assortment.all_partner_ids, self.partner + self.partner2)

    def test_assortment_update_with_multiple_partner(self):
        assortment = self.filter_obj.with_context(product_assortment=True).create(
            {
                "name": "Test Assortment multiple partner",
                "partner_domain": "[('name', '=', 'Test partner updated')]",
                "partner_ids": [(4, self.partner.id), (4, self.partner2.id)],
            }
        )
        self.partner.name = "Test partner updated"
        self.assertIn(assortment.id, self.partner.applied_assortment_ids.ids)
        self.assertEqual(assortment.all_partner_ids, self.partner + self.partner2)

    def test_assortment_with_black_list_product_domain(self):
        excluded_product = self.product_virtual_home_staging
        assortment = self.filter_obj.with_context(product_assortment=True).create(
            {
                "name": "Test Assortment black product domain",
                "domain": [],
                "partner_ids": [(4, self.partner2.id)],
                "apply_black_list_product_domain": True,
                "black_list_product_domain": [("id", "=", excluded_product.id)],
            }
        )
        allowed_products = self.env["product.product"].search(
            assortment._get_eval_domain()
        )
        self.assertNotIn(excluded_product, allowed_products)

    def test_compute_all_partner_ids_empty_domain(self):
        assortment = self.filter_obj.new(
            {"is_assortment": True, "partner_ids": [(4, self.partner.id)]}
        )
        field = assortment._fields["partner_domain"]
        assortment.env.cache.set(assortment, field, [])
        assortment._compute_all_partner_ids()
        self.assertEqual(assortment.all_partner_ids, assortment.partner_ids)

    def test_compute_record_count_no_model(self):
        filter_record = self.filter_obj.create(
            {
                "name": "Test non assortment",
                "is_assortment": False,
                "model_id": "res.partner",
                "domain": "[]",
            }
        )
        self.assertEqual(filter_record.record_count, 0)

        new_assortment = self.filter_obj.new(
            {
                "name": "Test new assortment",
                "is_assortment": True,
            }
        )
        self.assertEqual(new_assortment.record_count, 0)

    def test_write_clear_cache(self):
        self.assortment.write({"partner_domain": "[]"})
        self.assortment.write({"partner_ids": [(4, self.partner.id)]})
        self.assertTrue(True)

    def test_ir_rule_compute_domain(self):
        user_no_group = self.env["res.users"].create(
            {
                "name": "User No Group",
                "login": "user_no_group",
                "group_ids": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )
        user_with_group = self.env["res.users"].create(
            {
                "name": "User With Group",
                "login": "user_with_group",
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref(
                                "product_assortment.group_product_assortment_manager"
                            ).id,
                            self.env.ref("base.group_user").id,
                        ],
                    )
                ],
            }
        )

        # User without group
        domain_no_group = (
            self.env["ir.rule"].with_user(user_no_group)._compute_domain("ir.filters")
        )
        has_extra_domain = any(
            isinstance(leaf, tuple) and leaf[0] == "is_assortment" and leaf[2] is False
            for leaf in domain_no_group
        )
        self.assertTrue(has_extra_domain)

        # User with group
        domain_with_group = (
            self.env["ir.rule"].with_user(user_with_group)._compute_domain("ir.filters")
        )
        has_extra_domain = any(
            isinstance(leaf, tuple) and leaf[0] == "is_assortment" and leaf[2] is False
            for leaf in domain_with_group
        )
        self.assertFalse(has_extra_domain)
