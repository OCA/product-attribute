# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    active = fields.Boolean(default=True)

    @api.model
    def _cron_archive_product_supplierinfo(self):
        """Archive expired vendor pricelists."""
        today = fields.Date.today()
        sellers = self.env["product.supplierinfo"].search(
            [
                ("date_end", "!=", False),
                ("date_end", "<", today),
            ]
        )
        _logger.info("Archiving %s vendor pricelists", len(sellers))
        sellers.write({"active": False})
        return sellers
