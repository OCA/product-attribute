# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, fields, models
from odoo.fields import first

_logger = logging.getLogger(__name__)


class ProductPricelistAssortmentItem(models.Model):

    _name = "product.pricelist.assortment.item"
    _description = "Product Pricelist Assortment Item"
    _inherit = "product.pricelist.item"

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

    def _get_pricelist_item_name_price(self):
        super()._get_pricelist_item_name_price()
        for rec in self:
            if rec.assortment_filter_id:
                rec.name = rec.assortment_filter_id.name

    def _get_blacklist_columns(self):
        # fields to ignore to create pricelist item
        specific_columns = [
            "pricelist_id",
            "assortment_item_id",
            "applied_on",
            "product_id",
            "name",
            "display_name",
        ]
        return models.MAGIC_COLUMNS + [self.CONCURRENCY_CHECK_FIELD] + specific_columns

    def _get_pricelist_item_values(self, products_to_add=False):
        """
        Get a list of values to create new product.pricelist.item
        :return: list of dict
        """
        self.ensure_one()
        if not products_to_add:
            products_to_add = self.env["product.product"].browse()
        create_values = []
        blacklist = self._get_blacklist_columns()
        default_values = {
            k: self._fields.get(k).convert_to_write(self[k], self)
            for k in self.env["product.pricelist.item"]._fields.keys()
            if k not in blacklist
        }

        for product in products_to_add:
            values = default_values.copy()
            values.update(
                {
                    "pricelist_id": self.pricelist_id.id,
                    "assortment_item_id": self.id,
                    "applied_on": "0_product_variant",
                    "product_id": product.id,
                }
            )
            create_values.append(values)

        return create_values, default_values

    def _get_product_from_assortment(self):
        domain = self.assortment_filter_id._get_eval_domain()
        products = self.env[self.assortment_filter_id.model_id].search(domain)
        return products

    def _get_related_items(self):
        return self.mapped("pricelist_item_ids")

    def _get_assortment_changes(self):
        ProductProduct = self.env["product.product"]
        assortment_products = self._get_product_from_assortment()
        existing_products = self._get_related_items().mapped("product_id")
        if existing_products:
            products_to_add = assortment_products - existing_products
            products_to_remove = existing_products - assortment_products
            products_to_update = (
                assortment_products - products_to_add - products_to_remove
            )
        else:
            products_to_add = assortment_products
            products_to_remove = ProductProduct.browse()
            products_to_update = ProductProduct.browse()
        return products_to_add, products_to_update, products_to_remove

    def _check_need_update(self, item, update_value):
        need_update = False
        blacklist = self._get_blacklist_columns()
        values = {
            k: item._fields.get(k).convert_to_write(item[k], item)
            for k in item._fields.keys()
            if k not in blacklist
        }

        for key, val in update_value.items():
            need_update = bool(values[key] != val)
            if need_update:
                break
        return need_update

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

        (
            products_to_add,
            products_to_update,
            products_to_remove,
        ) = self._get_assortment_changes()

        create_values, update_values = self._get_pricelist_item_values(products_to_add)
        old_items = self._get_related_items()

        update_items = old_items.filtered(lambda x: x.product_id in products_to_update)
        item = first(update_items)
        if self._check_need_update(item, update_values):
            update_items.write(update_values)
        self.env["product.pricelist.item"].with_user(SUPERUSER_ID).create(create_values)
        remove_items = old_items.filtered(lambda x: x.product_id in products_to_remove)
        remove_items.unlink()
        return True
