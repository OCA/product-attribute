# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductProfile(TransactionCase):
    def setUp(self):
        super(TestProductProfile, self).setUp()
        self.prd_m = self.env["product.product"]
        # product 'HDD SH-2' in demo data
        self.hard_disc_prd = self.env.ref("product.product_product_17")
        self.my_own_profile = self.env.ref("product_profile_example.own")
        self.manufacturing_prof = self.env.ref(
            "product_profile_example.manuf_prof"
        )
        self.analysis_tmpl = self.env.ref(
            "point_of_sale.partner_product_7_product_template"
        )
        self.analysis_prd = self.env.ref("point_of_sale.partner_product_7")
        self.theoritical_categ_id = self.env.ref("product.product_category_5")
        self.categ = self.env.ref("product.product_category_3")

    def test_check_hard_disc_product(self):
        # check route_ids
        real_routes = [x.id for x in self.hard_disc_prd.route_ids]
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
            self.hard_disc_prd.categ_id.id, theoritical_categ_id.id
        )

    def test_create_product(self):
        name = "only name is specified"
        vals = {"profile_id": self.my_own_profile.id, "name": name}
        new_product = self.prd_m.create(vals)
        new_product._onchange_from_profile()
        count_prd = self.prd_m.search([("name", "=", name)])
        self.assertEqual(len(count_prd), 1)

    def test_write_template(self):
        vals = {"profile_id": self.my_own_profile.id}
        self.analysis_tmpl.write(vals)
        self.assertEqual(self.analysis_tmpl.profile_id, self.my_own_profile)

    def test_write_product(self):
        vals = {"profile_id": self.my_own_profile.id}
        self.analysis_prd.write(vals)
        self.assertEqual(self.analysis_prd.profile_id, self.my_own_profile)

    def test_product_tmpl_fields_view_get(self):
        view_id = self.env.ref("product.product_template_search_view").id
        res = self.hard_disc_prd.fields_view_get(
            view_id=view_id, view_type="search"
        )
        self.assertTrue(
            'string="My Own Type Saleable"' in res["arch"],
            'string="My Own Type Saleable" must be in '
            "fields_view_get() output",
        )

    def test_impact_write_profile_model(self):
        """If profile is updated, products must be written too
           on profile depends fields"""
        self.manufacturing_prof.write({"type": "consu"})
        product = self.env["product.product"].search(
            [("profile_id", "=", self.manufacturing_prof.id)]
        )[0]
        self.assertEqual(product.type, "consu")

    def test_default_behavior(self):
        """Check if field prefixed with default_profile
           have a default behavior on field values"""
        categ = self.categ
        consu_profile = self.env.ref("product_profile_example.consu_prof")
        vals = {
            "profile_id": consu_profile.id,
            "categ_id": categ.id,
            "name": "Product with modified category",
        }
        new_product = self.prd_m.create(vals)
        self.assertEqual(new_product.categ_id, categ)
