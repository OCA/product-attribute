# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def cron_recompute_bom_weight(self):
        products = self.recompute_bom_weight_search()
        batch_size = 1000
        # print('****')
        # import pdb;pdb.set_trace()

        for i in range(0, len(products), batch_size):

            products_batch = products[i : i + batch_size]
            products_batch.with_delay().update_weight_from_bom()
