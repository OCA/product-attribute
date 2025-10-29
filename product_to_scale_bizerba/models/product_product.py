# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    scale_group_id = fields.Many2one(
        "product.scale.group",
        related="product_tmpl_id.scale_group_id",
        store=True,
        readonly=False,
    )
    scale_sequence = fields.Integer(
        related="product_tmpl_id.scale_sequence",
        readonly=False,
        store=True,
    )
    scale_tare_weight = fields.Float(
        digits="Stock Weight",
        related="product_tmpl_id.scale_tare_weight",
        readonly=False,
        store=True,
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom.",
    )

    # View Section
    def send_scale_create(self):
        for product in self:
            self._send_to_scale_bizerba("create", product)
        return True

    def send_scale_write(self):
        for product in self:
            self._send_to_scale_bizerba("write", product)
        return True

    def send_scale_unlink(self):
        for product in self:
            self._send_to_scale_bizerba("unlink", product)
        return True

    # Custom Section
    def _send_to_scale_bizerba(self, action, product):
        log_date = fields.Datetime.now()
        ScaleLog = self.env["product.scale.log"]
        args = [
            ("log_date", "=", log_date),
            ("scale_system_id", "=", product.scale_group_id.scale_system_id.id),
            ("product_id", "=", product.ids[0]),
            ("action", "=", action),
        ]
        existing_logs = ScaleLog.search(args, limit=1)
        if not existing_logs:
            ScaleLog.create(
                {
                    "log_date": log_date,
                    "scale_system_id": product.scale_group_id.scale_system_id.id,
                    "product_id": product.ids[0],
                    "action": action,
                }
            )

    def _check_vals_scale_bizerba(self, vals, product):
        system = product.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = list(vals.keys())
        return set(system_fields).intersection(vals_fields)

    def _condition_bizerba_off(self):
        return self.env.context.get("bizerba_off", False)

    @api.onchange("lst_price")
    def _set_product_lst_price(self):
        return super(
            ProductProduct, self.with_context(bizerba_off=True)
        )._set_product_lst_price()

    # Overload Section
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        products = res.filtered("scale_group_id")
        if not self._condition_bizerba_off():
            for product in products:
                self._send_to_scale_bizerba("create", product)
        return res

    def write(self, vals):
        defered = {}
        if not self._condition_bizerba_off():
            for product in self:
                ignore = not product.scale_group_id and "scale_group_id" not in list(
                    vals.keys()
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
                            self._send_to_scale_bizerba("unlink", product)
                            # Create in the new group
                            defered[product.id] = "create"
                        elif vals.get("available_in_pos"):
                            defered[product.id] = "create"
                        elif (
                            product.available_in_pos
                            and self._check_vals_scale_bizerba(vals, product)
                        ):
                            # Data related to the scale
                            defered[product.id] = "write"

        res = super().write(vals)

        for product_id, action in defered.items():
            product = self.filtered(lambda p, pid=product_id: p.id == pid)
            if not product:
                continue
            self._send_to_scale_bizerba(action, product)

        return res

    def unlink(self):
        if not self._condition_bizerba_off():
            for product in self:
                if product.scale_group_id:
                    self._send_to_scale_bizerba("unlink", product)
        return super().unlink()
