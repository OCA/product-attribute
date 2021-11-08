# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("discontinued", "Discontinued"),
            ("phaseout", "Phase Out"),
            ("endoflife", "End-Of-Life"),
        ],
        compute="_compute_status",
    )
    # So the status can be displayed in the form and in the header
    # Without conflict
    status_display = fields.Selection(
        related="status", string="Product Status", readonly=True
    )
    end_of_life_date = fields.Date(
        string="End-of-life",
        help="When the product is end-of-life, and you want to warn your "
        "client/avoid order in the future.",
    )
    discontinued_until = fields.Date(
        string="Discontinued until",
        help="When the product is discontinued for a certain time, to warn "
        "your client/avoid order during this downtime.",
    )
    new_until = fields.Date(
        string="New until",
        help="New product, and you want to warn your client for a certain time",
    )

    @api.onchange("end_of_life_date")
    def _onchange_end_of_life_date(self):
        for rec in self:
            if rec.end_of_life_date:
                rec.update({"new_until": False, "discontinued_until": False})

    @api.onchange("discontinued_until")
    def _onchange_discontinued_until(self):
        for rec in self:
            if rec.discontinued_until:
                rec.update({"new_until": False})

    @api.depends("new_until", "end_of_life_date", "discontinued_until")
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if record.end_of_life_date:
                if record.end_of_life_date < today:
                    record.status = "endoflife"
                else:
                    record.status = "phaseout"
            elif (
                record.discontinued_until
                and record.discontinued_until >= today
            ):
                record.status = "discontinued"
            elif record.new_until and record.new_until >= today:
                record.status = "new"
            else:
                record.status = False
