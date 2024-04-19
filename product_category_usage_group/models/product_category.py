# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    usage_group_id = fields.Many2one(
        comodel_name="res.groups",
        string="Usage Group",
        help="If defined"
        ", the user should be member to this group, to use this product"
        " category when creating or updating products",
    )
