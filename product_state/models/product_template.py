# Copyright 2017-2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):

    _inherit = "product.template"

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
        default=lambda self: self._get_default_product_state().id,
        index=True,
        tracking=10,
    )

    def _inverse_product_state_id(self):
        """
        Allow to ease triggering other stuff when product state changes
        without a write()
        """

    @api.model
    def _get_default_product_state(self):
        return self.env["product.state"].search([("default", "=", True)], limit=1)

    @api.depends("product_state_id")
    def _compute_product_state(self):
        for product_tmpl in self:
            product_tmpl.state = product_tmpl.product_state_id.code

    def _inverse_product_state(self):
        for product_tmpl in self:
            self._set_product_state_id(product_tmpl)

    # This method can be called by variant so the record is either
    # product.template or product.product
    @api.model
    def _set_product_state_id(self, record):
        """ The record param is for similar state field at product.product model. """
        ProductState = record.env["product.state"]
        product_state = ProductState.search([("code", "=", record.state)], limit=1)
        if record.state and not product_state:
            msg = _("The product state code %s could not be found.")
            raise UserError(msg % record.state)
        record.product_state_id = product_state.id

    @api.model
    def _read_group_state_id(self, states, domain, order):
        return states.search([])
