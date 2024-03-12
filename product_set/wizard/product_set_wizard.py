# Copyright 2015 Anybox S.A.S
# Copyright 2016-2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductSetWizard(models.AbstractModel):
    _name = "product.set.wizard"
    _rec_name = "product_set_id"
    _description = "Transient base model to define custom wizards"

    partner_id = fields.Many2one("res.partner")
    product_set_id = fields.Many2one(
        "product.set", "Product set", required=True, ondelete="cascade"
    )
    product_set_line_ids = fields.Many2many(
        "product.set.line",
        string="Product set lines",
        required=True,
        store=True,
        ondelete="cascade",
        compute="_compute_product_set_line_ids",
        readonly=False,
    )
    quantity = fields.Float(
        digits="Product Unit of Measure", required=True, default=1.0
    )

    @api.depends("product_set_id")
    def _compute_product_set_line_ids(self):
        for rec in self:
            rec.product_set_line_ids = rec.product_set_id.set_line_ids

    def _get_lines(self):
        # hook here to take control on used lines
        for set_line in self.product_set_line_ids:
            yield set_line

    def _check_partner(self):
        """This method may be extended in other modules that use product_set as a base."""
        if not self.product_set_id.partner_id:
            return

    def add_set(self):
        """This method may be extended in other modules that use product_set as a base."""
        self._check_partner()
