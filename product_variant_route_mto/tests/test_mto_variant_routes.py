# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.fields import Command

from .common import TestMTOVariantCommon


class TestMTOVariantRoutes(TestMTOVariantCommon):
    def test_variant_created_on_mto_template(self):
        template = self.env["product.template"].create(
            {"name": "mto pen", "route_ids": [Command.link(self.mto_route.id)]}
        )
        self.assertTrue(template.is_mto)
        self.assertVariantsMTO(template.product_variant_ids)

    def test_variants_created_on_mto_template_with_attributes(self):
        template = self.env["product.template"].create(
            {
                "name": "mto pen",
                "route_ids": [Command.link(self.mto_route.id)],
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color.id,
                            "value_ids": [Command.set(self.values.ids)],
                        }
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 4)
        self.assertVariantsMTO(template.product_variant_ids)

    def test_variant_created_on_already_mto_template(self):
        self.template_pen.route_ids = [Command.link(self.mto_route.id)]
        self.assertVariantsMTO(self.variants_pen)
        value_white = self.env["product.attribute.value"].create(
            {"name": "white", "attribute_id": self.color.id}
        )
        self.template_pen.attribute_line_ids.value_ids = [Command.link(value_white.id)]
        white_pen = self.template_pen.product_variant_ids - self.variants_pen
        self.assertEqual(len(white_pen), 1)
        self.assertVariantsMTO(white_pen)

    def test_variant_created_with_mto_route(self):
        product = self.env["product.product"].create(
            {"name": "mto pen", "route_ids": [Command.link(self.mto_route.id)]}
        )
        self.assertVariantsMTO(product)
        self.assertNotIn(self.mto_route, product.product_tmpl_id.route_ids)

    def test_write_mto_route_on_variant(self):
        template_routes = self.template_pen.route_ids
        self.assertVariantsNotMTO(self.variants_pen)
        self.black_pen.route_ids = [Command.link(self.mto_route.id)]
        self.assertVariantsMTO(self.black_pen)
        self.assertVariantsNotMTO(self.blue_pen | self.red_pen | self.green_pen)
        # the mto route is carried by the variant, not by the template
        self.assertEqual(self.template_pen.route_ids, template_routes)

    def test_write_other_route_on_variant(self):
        template_routes = self.template_pen.route_ids
        route = self.env["stock.route"].create({"name": "other route"})
        self.black_pen.route_ids = [Command.link(route.id)]
        self.assertEqual(
            self.template_pen.route_ids.sorted(), (template_routes | route).sorted()
        )
        self.assertVariantsNotMTO(self.variants_pen)
