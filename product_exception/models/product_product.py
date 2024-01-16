# Copyright 2021 ForgeFlow (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.tools import config


class ProductProduct(models.Model):
    _inherit = ["product.product", "base.exception"]
    _name = "product.product"

    exception_ids = fields.Many2many(related="product_tmpl_id.exception_ids")

    def _get_main_records(self):
        return self.mapped("product_tmpl_id")

    @api.model
    def _fields_trigger_check_exception(self):
        return ["ignore_exception"]

    @api.model
    def _reverse_field(self):
        return "product_tmpl_ids"

    def _detect_exceptions(self, rule):
        """
        Return the Product Templates from the Product Variants that have
        Exceptions
        """
        records = super()._detect_exceptions(rule)
        return records.mapped("product_tmpl_id")

    def action_product_detect_exceptions(self):
        """
        Manually trigger to calculate the Exceptions. For Variants
        calculate for them only
        """
        self.detect_exceptions()
        return {"type": "ir.actions.act_window_close"}

    @api.model
    def create(self, vals):
        """
        Upon creation, check if the Product Variant has any Exception, if so,
        raise a Validation Error
        """
        record = super(ProductProduct, self).create(vals)
        check_exceptions = any(
            field in vals for field in self._fields_trigger_check_exception()
        )
        if check_exceptions:
            record.product_check_exception()
        return record

    def write(self, vals):
        """
        When changing one of the trigger fields, check if the Product Variant
        has any Exception, if so, raise a Validation Error
        """
        result = super(ProductProduct, self).write(vals)
        check_exceptions = any(
            field in vals for field in self._fields_trigger_check_exception()
        )
        if check_exceptions:
            self.product_check_exception()
        return result

    def product_check_exception(self):
        if (
            self
            and not self.env.context.get("skip_product_check_exception", False)
            and (
                not config["test_enable"]
                or self.env.context.get("test_product_check_exception", False)
            )
        ):
            self._check_exception()
