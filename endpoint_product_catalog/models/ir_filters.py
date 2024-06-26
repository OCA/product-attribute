# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class IrFilters(models.Model):
    _inherit = "ir.filters"

    endpoint_ids = fields.One2many("endpoint.endpoint", "product_assortment_id")
    endpoint_count = fields.Integer(compute="_compute_endpoint_count")

    @api.depends("endpoint_ids")
    def _compute_endpoint_count(self):
        for rec in self:
            rec.endpoint_count = len(rec.endpoint_ids)

    def action_view_endpoints(self):
        self.ensure_one()
        xmlid = "endpoint.endpoint_endpoint_act_window"
        return dict(
            self.env["ir.actions.act_window"]._for_xml_id(xmlid),
            name=_("Endpoints"),
            domain=[("product_assortment_id", "=", self.id)],
            context=dict(self.env.context, default_product_assortment_id=self.id),
        )
