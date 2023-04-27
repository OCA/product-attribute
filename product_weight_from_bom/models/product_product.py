# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def recompute_bom_weight_search(self):
        domain = [
            ("bom_ids", "!=", "False"),
        ]
        products = self.search(domain)
        return products

    def update_weight_from_bom(self):
        wizard = (
            self.env["product.weight.update"]
            .with_context(active_model="product.product", active_ids=self.ids)
            .create({})
        )
        wizard.update_multi_product_weight()

    def cron_recompute_bom_weight(self):
        products = self.recompute_bom_weight_search()
        products.update_weight_from_bom()
