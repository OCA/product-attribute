# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Custom Section
    @api.constrains("categ_id")
    def _check_usage_product_category(self):
        for record in self.filtered(lambda x: x.categ_id):
            category = record.categ_id
            group = category.usage_group_id
            if group and group.id not in self.env.user.groups_id.ids:
                raise ValidationError(
                    _(
                        'You can not use the product category "%(categname)s"'
                        ' because you are not member of the group "%(groupname)s"'
                        % {"categname": category.name, "groupname": group.name}
                    )
                )
