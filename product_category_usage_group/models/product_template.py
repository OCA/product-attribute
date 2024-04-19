# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Overload Section
    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list):
            if vals.get("categ_id"):
                template._check_usage_product_category(vals["categ_id"])
        return templates

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if vals.get("categ_id"):
            for rec in self:
                rec._check_usage_product_category(vals.get("categ_id"))
        return res

    # Custom Section
    def _check_usage_product_category(self, categ_id):
        ProductCategory = self.env["product.category"]
        if categ_id:
            category = ProductCategory.browse(categ_id)
            group = category.usage_group_id
            if group and group.id not in self.env.user.groups_id.ids:
                raise ValidationError(
                    _(
                        'You can not use the product category "%(categname)s"'
                        ' because you are not member of the group "%(groupname)s)"'
                        % {"categname": category.name, "groupname": group.name}
                    )
                )
