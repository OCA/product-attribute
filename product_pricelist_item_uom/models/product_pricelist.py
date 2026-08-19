# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.fields import Domain


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products, quantity, *, uom=None, **kwargs):
        self_with_uom = self.with_context(pricelist_item_uom_id=uom.id) if uom else self
        return super(ProductPricelist, self_with_uom)._compute_price_rule(
            products, quantity, uom=uom, **kwargs
        )

    def _get_applicable_rules_domain(self, products, date, **kwargs):
        domain = Domain(super()._get_applicable_rules_domain(products, date, **kwargs))
        uom_id = self.env.context.get("pricelist_item_uom_id")
        if uom_id:
            domain &= Domain("uom_id", "=", False) | Domain("uom_id", "=", uom_id)
        return domain

    def _get_related_uoms(self, product):
        """Return the packagings having their own rule in this pricelist.

        :param product: product template or product variant record.
        :return: UoMs defined on the matching pricelist items.
        :rtype: uom.uom
        """
        domain = self._get_applicable_rules_domain(
            product, fields.Datetime.now()
        ) & Domain("uom_id", "!=", False)
        return (
            self.env["product.pricelist.item"].search_fetch(domain, ["uom_id"]).uom_id
        )
