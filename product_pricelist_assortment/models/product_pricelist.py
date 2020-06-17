# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    item_assortment_ids = fields.One2many(
        comodel_name="product.pricelist.assortment.item",
        inverse_name="pricelist_id",
        string="Assortment items",
    )

    def action_launch_assortment_update(self):
        """
        Action to execute update of assortment items
        :return: dict
        """
        for item_assortment in self.mapped("item_assortment_ids"):
            item_assortment._update_assortment_items()
        return True

    @api.model
    def _get_pricelist_assortment_to_update(self):
        """
        Get every pricelists related to an assortment (and active)!
        :return: self recordset
        """
        return self.env["product.pricelist"].search(
            [("item_assortment_ids", "!=", False)]
        )

    @api.model
    def cron_assortment_update(self):
        pricelists = self._get_pricelist_assortment_to_update()
        pricelists.action_launch_assortment_update()
        return True
