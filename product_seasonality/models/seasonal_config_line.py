# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SeasonalConfigLine(models.Model):
    _name = "seasonal.config.line"
    _description = "Product seasonal configuration Line"

    seasonal_config_id = fields.Many2one(
        string="Product seasonal configuration",
        comodel_name="seasonal.config",
        required=True,
    )
    product_template_id = fields.Many2one(
        comodel_name="product.template",
        domain=[("sale_ok", "=", True)],
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('product_tmpl_id', '=', product_template_id)]",
    )
    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime()
    monday = fields.Boolean(default=True)
    tuesday = fields.Boolean(default=True)
    wednesday = fields.Boolean(default=True)
    thursday = fields.Boolean(default=True)
    friday = fields.Boolean(default=True)
    saturday = fields.Boolean(default=True)
    sunday = fields.Boolean(default=True)
    display_name = fields.Char(compute="_compute_display_name")

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        for line in self:
            if line.date_end and line.date_end < line.date_start:
                raise ValidationError(
                    _("The end date cannot be earlier than the start date.")
                )

    def is_sale_ok(self, date):
        self.ensure_one()

        weekday = date.strftime("%A").lower()
        # check if we are on the correct day of the week
        if not self[weekday]:
            return False

        date_end = self.date_end or date
        return self.date_start <= date <= date_end

    # TODO: shall we use the product's company to retrieve the default config?

    def find_for_product(self, prod, config=None):
        domain = [
            "|",
            ("product_id", "=", prod.id),
            "&",
            ("product_id", "=", False),
            ("product_template_id", "=", prod.product_tmpl_id.id),
        ]
        if config:
            domain.append(("seasonal_config_id", "=", config.id))
        return self.search(domain)

    @api.depends("seasonal_config_id", "product_template_id", "product_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec._name_get()

    def _name_get(self):
        parts = [
            f"[{self.seasonal_config_id.display_name}]",
            self.product_id.display_name or self.product_template_id.display_name,
            f"({self.id})",
        ]
        return " ".join(parts)
