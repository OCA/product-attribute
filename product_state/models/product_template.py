# Copyright 2017-2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.orm.domains import Domain


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
        copy=False,
    )

    def _inverse_product_state_id(self):
        """Allow triggering custom behaviors on ``product_state_id`` updates

        Hook method, can be overridden by inheriting modules
        """

    @api.model
    def _get_default_product_state(self):
        return self.env["product.state"].search(Domain("default", "=", True), limit=1)

    @api.depends("product_state_id")
    def _compute_product_state(self):
        for product_tmpl in self:
            product_tmpl.state = product_tmpl.product_state_id.code

    def _inverse_product_state(self):
        for product_tmpl in self:
            self._set_product_state_id(product_tmpl)

    @api.model
    def _set_product_state_id(self, record: models.Model):
        """Updates ``product_state_id`` on ``record``

        :param record: any recordset whose model defines field ``product_state_id``
            (eg: ``product.template`` or ``product.product``)
        """
        ProductState = record.env["product.state"]
        product_state = ProductState.search(Domain("code", "=", record.state), limit=1)
        if record.state and not product_state:
            raise UserError(
                self.env._(
                    "The product state code %(product_state)s could not be found.",
                    product_state=record.state,
                )
            )
        record.product_state_id = product_state.id

    @api.model
    def _read_group_state_id(self, states, domain):
        return states.search(Domain.TRUE)
