# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    state = fields.Char(
        string="Product Status",
        index=True,
        compute="_compute_product_state",
        inverse="_inverse_product_state",
        readonly=True,
        store=True,
    )
    product_state_id = fields.Many2one(
        comodel_name="product.state",
        string="State",
        help="Select a state for this product",
        group_expand="_read_group_state_id",
        inverse="_inverse_product_state_id",
        default=lambda self: self.product_tmpl_id._get_default_product_state().id,
        index=True,
        tracking=10,
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
    tmpl_end_of_life_date = fields.Date(
        string="Template End-of-life",
        related="product_tmpl_id.end_of_life_date",
    )
    tmpl_discontinued_until = fields.Date(
        string="Template Discontinued until",
        related="product_tmpl_id.discontinued_until",
    )
    tmpl_new_until = fields.Date(
        string="Template New until",
        related="product_tmpl_id.new_until",
    )
    has_status_date = fields.Boolean(
        compute="_compute_has_status_date",
        store=False,
    )

    @api.onchange("end_of_life_date")
    def _onchange_end_of_life_date(self):
        for rec in self:
            self.product_tmpl_id._update_dates_of_states(rec, "end_of_life_date")

    @api.onchange("discontinued_until")
    def _onchange_discontinued_until(self):
        for rec in self:
            self.product_tmpl_id._update_dates_of_states(rec, "discontinued_until")

    @api.depends(
        "product_state_id",
        "new_until",
        "end_of_life_date",
        "discontinued_until",
        "product_tmpl_id.new_until",
        "product_tmpl_id.end_of_life_date",
        "product_tmpl_id.discontinued_until",
    )
    def _compute_product_state(self):
        for record in self:
            self.product_tmpl_id._check_dates_of_states(record)

    def _inverse_product_state(self):
        for product in self:
            self.product_tmpl_id._set_product_state_id(product)

    def _inverse_product_state_id(self):
        """
        Allow to ease triggering other stuff when product state changes
        without a write()
        """

    @api.model
    def _read_group_state_id(self, states, domain, order):
        return states.search([])

    def _compute_has_status_date(self):
        for rec in self:
            res = rec.end_of_life_date or rec.discontinued_until or rec.new_until
            rec.has_status_date = bool(res)
