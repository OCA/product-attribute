# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    weekly_sold_delivered = fields.Char(
        compute="_compute_weekly_sold_delivered",
        groups="sales_team.group_sale_salesman",
        readonly=True,
    )
    weekly_sold_delivered_shown = fields.Char(
        string="Weekly Sold",
        compute="_compute_weekly_sold_delivered_shown",
        groups="sales_team.group_sale_salesman",
    )

    @api.depends("weekly_sold_delivered")
    def _compute_weekly_sold_delivered_shown(self):
        """This fields is meant to be used only for display purposes so we can
        use custom characters show the sales stream. We want to keep the stored
        one as base 2 string so we can perform bitwise operations easily"""
        params = self.env["ir.config_parameter"].sudo()
        sold_char = params.get_param("product_sold_by_delivery_week.sold_char", "●")
        not_sold_char = params.get_param(
            "product_sold_by_delivery_week.not_sold_char", "◌"
        )
        not_service_products = self.filtered(lambda x: x.type != "service")
        (self - not_service_products).weekly_sold_delivered_shown = False
        for product in self.filtered(lambda x: x.type != "service"):
            product.weekly_sold_delivered_shown = (
                product.weekly_sold_delivered
                and "".join(
                    [
                        int(c) and sold_char or not_sold_char
                        for c in product.weekly_sold_delivered
                    ]
                )
            )

    @api.depends_context("force_company")
    @api.depends("product_variant_ids.weekly_sold_delivered")
    def _compute_weekly_sold_delivered(self):
        """Perform a bitwise operation over the variant values to easily check
        whether or not any of them has been sold"""
        params = self.env["ir.config_parameter"].sudo()
        weeks_to_consider = params.get_param(
            "product_sold_by_delivery_week.weeks_to_consider", 6
        )
        self.weekly_sold_delivered = False
        for product in self.filtered(lambda x: x.type != "service"):
            if len(product.product_variant_ids) == 1:
                product.weekly_sold_delivered = (
                    product.product_variant_ids.weekly_sold_delivered
                )
            variants_weekly_sold_delivered = product.product_variant_ids.mapped(
                "weekly_sold_delivered"
            )
            if not variants_weekly_sold_delivered:
                continue
            # The computed value is stored in the form of '0' and '1' strings so
            # bitwise operations are easilly done.
            weekly_sold_delivered = int(
                variants_weekly_sold_delivered.pop() or "0", base=2
            )
            while variants_weekly_sold_delivered:
                weekly_sold_delivered = weekly_sold_delivered | int(
                    variants_weekly_sold_delivered.pop() or "0", base=2
                )
            product.weekly_sold_delivered = "{:0{}b}".format(
                weekly_sold_delivered, weeks_to_consider
            )
