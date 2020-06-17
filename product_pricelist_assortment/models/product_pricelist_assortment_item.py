# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, fields, models

_logger = logging.getLogger(__name__)


class ProductPricelistAssortmentItem(models.Model):

    _name = "product.pricelist.assortment.item"
    _description = "Product Pricelist Assortment Item"
    _inherit = "product.pricelist.item"

    name = fields.Char(related="assortment_filter_id.name", readonly=True,)
    assortment_filter_id = fields.Many2one(
        comodel_name="ir.filters",
        domain=[("is_assortment", "=", True)],
        string="Assortment",
        ondelete="restrict",
        required=True,
    )
    pricelist_item_ids = fields.One2many(
        comodel_name="product.pricelist.item",
        inverse_name="assortment_item_id",
        help="Pricelist items created automatically",
    )

    def _get_pricelist_item_values(self):
        """
        Get a list of values to create new product.pricelist.item
        :return: list of dict
        """
        self.ensure_one()
        products = self._get_product_from_assortment()
        list_values = []
        # fields to ignore to create pricelist item
        blacklist = models.MAGIC_COLUMNS + [self.CONCURRENCY_CHECK_FIELD]
        blacklist.extend(["assortment_filter_id", "pricelist_item_ids"])
        default_values = {
            k: self._fields.get(k).convert_to_write(self[k], self)
            for k in self._fields.keys()
            if k not in blacklist
        }
        for product in products:
            values = default_values.copy()
            values.update(
                {
                    "pricelist_id": self.pricelist_id.id,
                    "assortment_item_id": self.id,
                    "applied_on": "0_product_variant",
                    "product_id": product.id,
                }
            )
            list_values.append(values)
        return list_values

    def _get_product_from_assortment(self):
        domain = self.assortment_filter_id._get_eval_domain()
        products = self.env[self.assortment_filter_id.model_id].search(domain)
        return products

    def _get_related_items(self):
        return self.mapped("pricelist_item_ids")

    def _update_assortment_items(self):
        """
        Update the pricelist with current assortment:
        - Prepare values for new assorment items;
        - Delete previous items.
        - Create new assortments items;

        :return: bool
        """
        self.ensure_one()
        if not self.assortment_filter_id.active:
            _logger.info(
                "The assortment item %s is ignored because the "
                "related assortment/filter is not active",
                self.display_name,
            )
            return False

        items_values = self._get_pricelist_item_values()
        old_items = self._get_related_items()
        old_items.unlink()
        self.env["product.pricelist.item"].with_user(SUPERUSER_ID).create(items_values)
        return True
