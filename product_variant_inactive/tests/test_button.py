# © 2017 Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):
    def test_fields_view_get_tree(self):
        product = self.help_create_product()
        product = product.with_context({"search_disable_custom_filters": True})
        root = etree.fromstring(product.fields_view_get()["arch"])
        for button in root.findall(".//button"):
            self.assertEquals("0", button.get("invisible", "0"))

    def test_fields_view_get_form(self):
        # button should appear if we have only 1 active product,
        # and n other inactive products
        product_template = self.env["product.template"].create(
            {"name": "product template with two variants"}
        )
        self.env["product.product"].create(
            {
                "name": "active product",
                "product_tmpl_id": product_template.id,
                "active": True,
            }
        )
        self.env["product.product"].create(
            {
                "name": "inactive product",
                "product_tmpl_id": product_template.id,
                "active": False,
            }
        )
        button_action_ref = self.env.ref("product.product_variant_action").id
        root = etree.fromstring(product_template.fields_view_get()["arch"])
        button = root.findall(".//button[@name='%d']" % button_action_ref)[0]
        self.assertEquals("0", button.get("invisible", "0"))

    def test_button_activate(self):
        self.help_button_active(False)

    def test_button_deactivate(self):
        self.help_button_active(True)

    def help_button_active(self, active=True):
        product = self.help_create_product(active)
        if active:
            product.button_deactivate()
        else:
            product.button_activate()
        self.assertEqual(product.active, not (active))

    def help_create_product(self, active=True):
        product = self.env["product.product"].create(
            {"active": active, "name": "test_product"}
        )
        return product

    def test_create_variant_do_not_reactivate(self):
        """Ensure that re-generating variants does not
        change the "active" state of the existing variant"""
        product = self.env.ref("product.product_product_4")
        product.active = False
        product.product_tmpl_id.create_variant_ids()
        self.assertEquals(product.active, False)
