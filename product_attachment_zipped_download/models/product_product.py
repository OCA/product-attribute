# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Productproduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "ir.attachment.action_download"]

    def _get_downloadable_attachments(self):
        """Overwrite to get the attachments from template or variants."""
        return self.env["ir.attachment"].search(
            [
                "|",
                "&",
                ("res_model", "=", "product.product"),
                ("res_id", "in", self.ids),
                "&",
                ("res_model", "=", "product.template"),
                ("res_id", "in", self.product_tmpl_id.ids),
            ]
        )
