# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.osv.expression import TERM_OPERATORS_NEGATION


class ProductTemplate(models.Model):

    _inherit = "product.template"

    not_followed = fields.Boolean(
        default=False,
        company_dependent=True,
        help="Check to set the product as notfollowed.",
        tracking=10,
    )

    followed = fields.Boolean(compute="_compute_followed", search="_search_followed")

    @api.depends("not_followed")
    def _compute_followed(self):
        for product in self:
            product.followed = not product.not_followed

    @api.model
    def _search_followed(self, operator, value):
        """
        Search function for the field mto_procurement.
        :param operator: str
        :param value: str
        :return: list of tuple (domain)
        """

        res_operator = TERM_OPERATORS_NEGATION[operator]
        return [("not_followed", res_operator, value)]
