# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    scale_group_id = fields.Many2one("product.scale.group")
    scale_sequence = fields.Integer()
    scale_tare_weight = fields.Float(
        digits="Stock Weight",
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom.",
    )

    def send_scale_create(self):
        for product in self:
            product.product_variant_ids.send_scale_create()
        return True

    def send_scale_write(self):
        for product in self:
            product.product_variant_ids.send_scale_write()
        return True

    def send_scale_unlink(self):
        for product in self:
            product.product_variant_ids.send_scale_unlink()
        return True

    def _condition_bizerba_off(self):
        return self.env.context.get("bizerba_off", False)

    def write(self, vals):
        product_obj = self.env["product.product"]
        context = self.env.context
        defered = {}
        if not context.get("create_product_product"):
            for template in self:
                for product in template.product_variant_ids:
                    ignore = (
                        not product.scale_group_id
                        and "scale_group_id" not in list(vals.keys())
                    )
                    if not ignore:
                        is_continue = False
                        if "active" in vals and not vals.get("active"):
                            # Unlink when deactivate
                            is_continue = True
                        elif (
                            product.available_in_pos
                            and "available_in_pos" in vals
                            and not vals.get("available_in_pos")
                        ):
                            is_continue = True

                        if is_continue:
                            defered[product.id] = "unlink"
                            continue

                        if not product.scale_group_id or vals.get("active"):
                            # (the product is new on this group)
                            defered[product.id] = "create"
                        elif not product.active:
                            continue
                        else:
                            if vals.get("scale_group_id", False) and (
                                vals.get("scale_group_id", False)
                                != product.scale_group_id.id
                            ):
                                # (the product has moved from a group to another)
                                # Remove from obsolete group
                                product_obj._send_to_scale_bizerba("unlink", product)
                                # Create in the new group
                                defered[product.id] = "create"
                            elif vals.get("available_in_pos"):
                                defered[product.id] = "create"
                            elif (
                                product.available_in_pos
                                and product_obj._check_vals_scale_bizerba(vals, product)
                            ):
                                # Data related to the scale
                                defered[product.id] = "write"

        res = super().write(vals)

        for product_id, action in defered.items():
            product = product_obj.browse(product_id)
            product_obj._send_to_scale_bizerba(action, product)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        templates = res.filtered("scale_group_id")
        if templates and not self._condition_bizerba_off():
            templates.send_scale_create()
        return res

    def unlink(self):
        templates = self.filtered("scale_group_id")
        if templates and not self._condition_bizerba_off():
            templates.send_scale_unlink()
        return super().unlink()
