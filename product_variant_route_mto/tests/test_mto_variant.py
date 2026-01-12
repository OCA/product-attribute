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
