# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo.exceptions import ValidationError
from odoo.tests import Form, SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestProductStatusCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_13")
        # To avoid error with filestore and Form test
        cls.product.image_1920 = False

    def test_default(self):
        self.assertEqual(self.product.status.code, False)

    @freeze_time("2020-09-15")
    def test_new(self):
        self.product.new_until = "2020-09-16"
        self.assertEqual(self.product.status.code, "new")
        self.product.new_until = "2020-09-14"
        self.assertEqual(self.product.status.code, False)

    @freeze_time("2020-09-15")
    def test_discontinued(self):
        self.product.discontinued_until = "2020-09-16"
        self.assertEqual(self.product.status.code, "discontinued")
        self.product.discontinued_until = "2020-09-14"
        self.assertEqual(self.product.status.code, False)

    @freeze_time("2020-09-15")
    def test_eol(self):
        self.product.end_of_life_date = "2020-09-14"
        self.assertEqual(self.product.status.code, "endoflife")
        self.product.end_of_life_date = "2020-09-16"
        self.assertEqual(self.product.status.code, "phaseout")

    @freeze_time("2020-09-15")
    def test_priority(self):
        # by order of importance: end_of_life_date, discontinued_until, new_until
        self.product.write(
            {
                "end_of_life_date": "2020-09-14",
                "discontinued_until": "2020-09-16",
                "new_until": "2020-09-16",
            }
        )
        # all set, EOL wins
        self.assertEqual(self.product.status.code, "endoflife")
        self.product.end_of_life_date = False
        # discontinued wins
        self.assertEqual(self.product.status.code, "discontinued")
        self.product.discontinued_until = False
        self.assertEqual(self.product.status.code, "new")

    @freeze_time("2020-09-15")
    def test_onchange(self):
        with Form(self.product) as form:
            form.new_until = "2020-09-16"
            self.assertEqual(form.status.code, "new")
            form.discontinued_until = "2020-09-16"
            self.assertEqual(form.status.code, "discontinued")
            # new_until wiped
            self.assertFalse(form.new_until)
            form.end_of_life_date = "2020-09-14"
            self.assertEqual(form.status.code, "endoflife")
            # other fields wiped when setting EOL
            self.assertFalse(form.new_until)
            self.assertFalse(form.discontinued_until)

    def test_modified_default_data(self):
        st_env = self.env["product.state"]
        default_state = st_env._get_default_data()
        vals = {"name": "State change", "code": "Code change"}
        for ds_id in default_state:
            vals["code"] = ds_id.code
            with self.assertRaises(ValidationError) as cm:
                st_env.browse(ds_id.id).write(vals)
            wn_expect = cm.exception.args[0]
            self.assertEqual(
                "Cannot modified default state, state name: %s" % (ds_id.name),
                wn_expect,
            )
            with self.assertRaises(ValidationError) as cm:
                st_env.browse(ds_id.id).unlink()
            wn_expect = cm.exception.args[0]
            self.assertEqual(
                "Cannot delete default state, state name: %s" % (ds_id.name), wn_expect
            )
