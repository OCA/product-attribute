# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if "active" in vals and\
                not self.env.context.get("product_propagate_active"):

            # initialize two empty list
            # Note: set "product_propagate_active" in the context to avoid
            # infinite loop, when writing on template model
            to_disable = to_enable =\
                self.env["product.template"].with_context(
                    product_propagate_active=True)
            for template in self.mapped("product_tmpl_id"):
                variant_values = template.with_context(
                    active_test=False).mapped('product_variant_ids.active')
                if template.active and not any(variant_values):
                    to_disable |= template
                elif not template.active and any(variant_values):
                    to_enable |= template

            if to_disable:
                to_disable.write({"active": False})
            if to_enable:
                to_enable.write({"active": True})

        return res
