# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from odoo import Command
from odoo.exceptions import ValidationError

from .common import TestMTOVariantCommon

onchange_logger = "odoo.tests.form.onchange"

_logger = logging.getLogger(onchange_logger)


class TestMTOVariant(TestMTOVariantCommon):
    def test_variants_mto(self):
        # instanciate variables
        pen_template = self.template_pen
        pens = self.variants_pen
        blue_pen = self.blue_pen
        red_pen = self.red_pen
        green_pen = self.green_pen
        black_pen = self.black_pen
        self.assertVariantsNotMTO(pens)
        # enable mto route for black pen
        self.toggle_is_mto(black_pen)
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(blue_pen | green_pen | red_pen)
        # enable mto route for black and blue pens
        self.toggle_is_mto(blue_pen)
        self.assertVariantsMTO(black_pen | blue_pen)
        self.assertVariantsNotMTO(red_pen | green_pen)
        # Now enable the mto route for the template, all variants get is_mto = True
        with self.assertLogs(onchange_logger, level="WARNING"):
            self.add_route(pen_template, self.mto_route)
        self.assertVariantsMTO(pens)
        # Disable mto route for black_pen
        with self.assertRaises(ValidationError):
            self.toggle_is_mto(black_pen)
        # Disable mto route on the template, reset is_mto on variants
        with self.assertLogs(onchange_logger, level="WARNING"):
            self.remove_route(pen_template, self.mto_route)
        self.assertVariantsNotMTO(pens)

    def test_variants_routes_updated(self):
        blue_pen = self.blue_pen
        self.assertVariantsNotMTO(blue_pen)
        blue_pen.route_ids = [Command.link(self.mto_route.id)]
        self.assertVariantsMTO(blue_pen)
        blue_pen.route_ids = [Command.clear()]
        self.assertVariantsNotMTO(blue_pen)

    def test_template_routes_updated(self):
        # instanciate variables
        pen_template = self.template_pen
        pens = self.variants_pen
        blue_pen = self.blue_pen
        red_pen = self.red_pen
        green_pen = self.green_pen
        black_pen = self.black_pen
        self.assertVariantsNotMTO(pens)
        # Now toggle a variant to is_mto
        self.toggle_is_mto(black_pen)
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(green_pen | red_pen | blue_pen)
        # Now modifying template.route_ids to trigger variant's _compute_is_mto
        random_route = self.mto_route.create({"name": "loutourout de la vit"})
        self.add_route(pen_template, random_route)
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(green_pen | red_pen | blue_pen)
        self.remove_route(pen_template, random_route)
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(green_pen | red_pen | blue_pen)

    def test_template_warnings(self):
        # instanciate variables
        pen_template = self.template_pen
        pens = self.variants_pen
        blue_pen = self.blue_pen
        red_pen = self.red_pen
        green_pen = self.green_pen
        black_pen = self.black_pen
        self.assertVariantsNotMTO(pens)

        # enable mto route for black pen
        self.toggle_is_mto(black_pen)
        self.assertVariantsMTO(black_pen)

        # Enable mto route on the template, raise warning as is_mto is reset on variants
        with self.assertLogs(onchange_logger, level="WARNING") as log_catcher:
            self.add_route(pen_template, self.mto_route)
        self.assertIn("WARNING", log_catcher.output[0])
        self.assertIn("Activating MTO route will reset", log_catcher.output[0])
        self.assertVariantsMTO(pens)

        # Enable unrelated route does not raise warning nor reset
        random_route = self.mto_route.create({"name": "loutourout de la vit"})
        with self.assertLogs(onchange_logger) as log_catcher:
            self.add_route(pen_template, random_route)
            _logger.info("No warning raised")
        self.assertNotIn("WARNING", log_catcher.output[0])
        self.assertVariantsMTO(pens)

        # Disable mto route on the template,
        # raise warning as is_mto is reset on variants
        with self.assertLogs(onchange_logger) as log_catcher:
            self.remove_route(pen_template, self.mto_route)
        self.assertIn("WARNING", log_catcher.output[0])
        self.assertIn("Deactivating MTO route will reset", log_catcher.output[0])
        self.assertVariantsNotMTO(pens)

        # Enable mto route for black pen
        self.toggle_is_mto(black_pen)
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(blue_pen | green_pen | red_pen)

        # Disable unrelated route does not raise warning nor reset
        with self.assertLogs(onchange_logger) as log_catcher:
            self.remove_route(pen_template, random_route)
            _logger.info("No warning raised")
        self.assertVariantsMTO(black_pen)
        self.assertVariantsNotMTO(blue_pen | green_pen | red_pen)

    def test_coverage_additional(self):
        # 1. Cover tests/common.py lines 65 and 71 by passing route=None
        pen_template = self.template_pen
        self.add_route(pen_template, None)
        self.remove_route(pen_template, None)

        # 2. Cover models/product_template.py line 40: no active mto route
        # Deactivate MTO routes temporarily
        mto_routes = self.env["stock.route"].search([("is_mto", "=", True)])
        mto_routes.write({"active": False})
        # Trigger onchange
        pen_template.onchange_route_ids()
        # Restore active state
        mto_routes.write({"active": True})

        # 3. Cover models/product_product.py line 74: non-MTO route inverse change
        blue_pen = self.blue_pen
        random_route = self.mto_route.create(
            {"name": "unrelated route", "product_selectable": True}
        )
        blue_pen.route_ids = [Command.link(random_route.id)]
        self.assertIn(random_route, blue_pen.product_tmpl_id.route_ids)

        # 4. Cover models/product_product.py lines 50-61 (Search route_ids)
        Product = self.env["product.product"]
        # operator '=' with recordset
        Product._search_route_ids(operator="=", value=self.mto_route)
        # operator '=' with list/iterable
        Product._search_route_ids(operator="=", value=[self.mto_route.id])
        # operator '=' with single integer ID
        Product._search_route_ids(operator="=", value=self.mto_route.id)
        # operator 'in' with single integer ID (covers line 66)
        Product._search_route_ids(operator="in", value=self.mto_route.id)
        # operator 'in' with recordset (covers line 62)
        Product._search_route_ids(operator="in", value=self.mto_route)
        # Search using 'in' operator with a list of routes including MTO route
        Product.search([("route_ids", "in", [self.mto_route.id, random_route.id])])
