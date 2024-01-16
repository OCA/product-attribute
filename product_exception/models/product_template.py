# Copyright 2019 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import config


class ProductTemplate(models.Model):
    _inherit = ["product.template", "base.exception"]
    _name = "product.template"

    @api.model
    def check_product_template_cron(self):
        products = self.env["product.template"].search([])
        for product in products:
            product.detect_exceptions()

    @api.model
    def _fields_trigger_check_exception(self):
        return ["ignore_exception"]

    @api.model
    def _reverse_field(self):
        return "product_tmpl_ids"

    def detect_exceptions(self):
        all_exceptions = super(ProductTemplate, self).detect_exceptions()
        products = self.mapped("product_variant_ids")
        all_exceptions += products.detect_exceptions()
        return all_exceptions

    def action_product_detect_exceptions(self):
        """
        Manually trigger to calculate the Exceptions. For Templates, calculate
        for them and for their respective Product Variants
        """
        self.detect_exceptions()
        return {"type": "ir.actions.act_window_close"}

    @api.model
    def create(self, vals):
        """
        Upon creation, check if the Product Template has any Exception, if so,
        raise a Validation Error
        """
        record = super(ProductTemplate, self).create(vals)
        check_exceptions = any(
            field in vals for field in self._fields_trigger_check_exception()
        )
        if check_exceptions:
            record.product_check_exception()
        return record

    def write(self, vals):
        """
        When changing one of the trigger fields, check if the Product Template
        has any Exception, if so, raise a Validation Error
        """
        result = super(ProductTemplate, self).write(vals)
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
