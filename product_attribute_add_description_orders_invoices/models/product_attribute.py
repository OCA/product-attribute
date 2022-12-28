# Copyright 2022 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    show_in_sale_invoices = fields.Boolean(
        string="Show Description In Orders & Invoices",
        help="This field allows to show this attribute in the description of sale "
        "order lines and invoice lines.",
    )
