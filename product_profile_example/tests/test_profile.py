# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductProfile(TransactionCase):
    def setUp(self):
        super(TestProductProfile, self).setUp()
        self._setup_obj_data()
        self._setup_profile_data()

    def _setup_obj_data(self):
        self.tmpl_m = self.env["product.template"]
        self.prd_m = self.env["product.product"]
        # misc
        self.desk_combination_prd = self.env.ref("product.product_product_3")
        self.analysis_tmpl = self.env.ref(
            "product.expense_hotel_product_template"
        )
        self.analysis_prd = self.env.ref("product.expense_hotel")
        self.theoritical_categ_id = self.env.ref("product.product_category_5")
        self.categ = self.env.ref("product.product_category_3")

    def _setup_profile_data(self):
        self.profile_own = self.env.ref("product_profile_example.profile_own")
        self.profile_own_nondefaults = {
            "type": "product",
            "sale_ok": True,
            "purchase_ok": False,
            "available_in_pos": True,
        }
        self.profile_own_defaults = {
            "categ_id": self.env.ref("product.product_category_all"),
            "route_ids": self.env.ref("purchase_stock.route_warehouse0_buy"),
        }
        self.profile_complete = self.env.ref(
            "product_profile_example.profile_complete"
        )
        self.profile_complete_nondefaults = {
            "type": "product",
            "sale_ok": True,
            "purchase_ok": True,
            "available_in_pos": True,
        }
        self.profile_complete_defaults = {
            "categ_id": self.env.ref("product.product_category_all"),
            "route_ids": [
                self.env.ref("mrp.route_warehouse0_manufacture")
                + self.env.ref("stock.route_warehouse0_mto")
                + self.env.ref("purchase_stock.route_warehouse0_buy")
            ],
        }
        self.profile_manuf = self.env.ref(
            "product_profile_example.profile_manuf"
        )

    def test_check_desk_combination_product(self):
        # check route_ids
        real_routes = [x.id for x in self.desk_combination_prd.route_ids]
        theoritical_routes = [
            self.env.ref("mrp.route_warehouse0_manufacture").id,
            self.env.ref("stock.route_warehouse0_mto").id,
        ]
        real_routes.sort()
        theoritical_routes.sort()
        self.assertEqual(real_routes, theoritical_routes)
        # check categ_id
        theoritical_categ_id = self.theoritical_categ_id
        self.assertEqual(
            self.desk_combination_prd.categ_id.id, theoritical_categ_id.id
        )

    def test_on_create_template_with_profile(self):
        """Creating a product with a profile applies all the profile's values"""
        name = "template with 'own' profile"
        vals = {"profile_id": self.profile_own.id, "name": name}
        new_tmpl = self.tmpl_m.create(vals)
        count_tmpl = self.tmpl_m.search([("name", "=", name)]).ids
        self.assertEqual(len(count_tmpl), 1)
        # test all values from profile are applied
        for key in self.profile_own_nondefaults:
            self.assertEqual(
                self.profile_own_nondefaults[key], getattr(new_tmpl, key)
            )
        for key in self.profile_own_defaults:
            self.assertEqual(
                self.profile_own_defaults[key], getattr(new_tmpl, key)
            )

    def test_on_create_product_with_profile(self):
        """Creating a product with a profile applies all the profile's values"""
        name = "product with 'own' profile"
        vals = {"profile_id": self.profile_own.id, "name": name}
        new_prd = self.prd_m.create(vals)
        count_prd = self.prd_m.search([("name", "=", name)]).ids
        self.assertEqual(len(count_prd), 1)
        # test all values from profile are applied
        for key in self.profile_own_nondefaults:
            self.assertEqual(
                self.profile_own_nondefaults[key], getattr(new_prd, key)
            )
        for key in self.profile_own_defaults:
            self.assertEqual(
                self.profile_own_defaults[key], getattr(new_prd, key)
            )

    def test_on_set_tmpl_profile(self):
        """Test that setting a profile impacts:
         - nondefaults in every case
         - defaults only if there was no profile previously"""

        # set profile to "own"
        vals = {"profile_id": self.profile_own.id}
        self.analysis_tmpl.write(vals)
        self.assertEqual(self.analysis_tmpl.profile_id, self.profile_own)
        for key in self.profile_own_nondefaults:
            self.assertEqual(
                self.profile_own_nondefaults[key],
                getattr(self.analysis_tmpl, key),
            )
        for key in self.profile_own_defaults:
            self.assertEqual(
                self.profile_own_defaults[key],
                getattr(self.analysis_tmpl, key),
            )

        # get vals on the template
        defaults_keys = self.profile_own_defaults.keys()
        defaults_tmpl_vals = {
            key: self.analysis_tmpl[key] for key in defaults_keys
        }

        # set profile to "complete_prof"
        vals = {"profile_id": self.profile_complete.id}
        self.analysis_tmpl.write(vals)
        self.assertEqual(self.analysis_tmpl.profile_id, self.profile_complete)
        for key in self.profile_complete_nondefaults:
            self.assertEqual(
                self.profile_complete_nondefaults[key],
                getattr(self.analysis_tmpl, key),
            )
        for key in self.profile_own_defaults:
            self.assertEqual(
                defaults_tmpl_vals[key], getattr(self.analysis_tmpl, key)
            )

    def test_on_set_prd_profile(self):
        """Test that setting a profile impacts:
         - nondefaults in every case
         - defaults only if there was no profile previously"""

        # set profile to "own"
        vals = {"profile_id": self.profile_own.id}
        self.analysis_prd.write(vals)
        self.assertEqual(self.analysis_prd.profile_id, self.profile_own)
        for key in self.profile_own_nondefaults:
            self.assertEqual(
                self.profile_own_nondefaults[key],
                getattr(self.analysis_prd, key),
            )
        for key in self.profile_own_defaults:
            self.assertEqual(
                self.profile_own_defaults[key], getattr(self.analysis_prd, key)
            )

        # get vals on the products
        defaults_keys = self.profile_own_defaults.keys()
        defaults_prd_vals = {
            key: self.analysis_tmpl[key] for key in defaults_keys
        }

        # set profile to "complete_prof"
        vals = {"profile_id": self.profile_own.id}
        self.analysis_prd.write(vals)
        self.assertEqual(self.analysis_prd.profile_id, self.profile_own)
        for key in self.profile_complete_nondefaults:
            self.assertEqual(
                self.profile_own_nondefaults[key],
                getattr(self.analysis_prd, key),
            )
        for key in self.profile_complete_defaults:
            self.assertEqual(
                defaults_prd_vals[key], getattr(self.analysis_prd, key)
            )

    def test_on_write_profile_nondefaults(self):
        """Writing on non-default profile fields should propagate
        changes on products"""
        product = self.env["product.product"].search(
            [("profile_id", "=", self.profile_manuf.id)]
        )[0]
        self.profile_manuf.write({"purchase_ok": False})
        self.assertEqual(product.purchase_ok, False)

    def test_on_write_profile_defaults(self):
        """Writing on default profile fields should not propagate
        changes on products"""
        product = self.env["product.product"].search(
            [("profile_id", "=", self.profile_manuf.id)]
        )[0]
        self.profile_manuf.write({"profile_default_categ_id": self.categ.id})
        self.assertNotEqual(product.categ_id, self.categ)

    def test_product_tmpl_fields_view_get(self):
        # test search filters loaded
        view_id = self.env.ref("product.product_template_search_view").id
        res = self.desk_combination_prd.fields_view_get(
            view_id=view_id, view_type="search"
        )
        self.assertTrue(
            b'string="My Own Type Saleable"' in res["arch"],
            'string="My Own Type Saleable" must be in '
            "fields_view_get() output",
        )
