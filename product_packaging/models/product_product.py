# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    packaging_ids = fields.One2many(
        comodel_name="product.packaging",
        inverse_name="product_id",
        string="Packaging",
    )

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        # New variants must inherit their template's packaging UoMs (create-only,
        # so variants created directly with ``packaging_ids`` keep them).
        products._create_missing_packagings()
        # An explicitly provided ``uom_ids`` gets wiped by its own recompute
        # while the variant is created (no packaging exists yet); re-apply it
        # now to materialize the packagings.
        for product, vals in zip(products, vals_list, strict=True):
            if uom_ids := vals.get("uom_ids"):
                product.uom_ids = uom_ids
        return products

    def _create_missing_packagings(self):
        """Create the packagings for the template UoMs not yet present.

        Create-only: never removes packagings, so a variant created directly
        with ``packaging_ids`` keeps them even when ``uom_ids`` is not set yet.
        """
        to_create = []
        for product in self:
            target_uoms = product.product_tmpl_id.uom_ids
            for uom in target_uoms - product.packaging_ids.uom_id:
                to_create.append({"product_id": product.id, "uom_id": uom.id})
        if to_create:
            self.env["product.packaging"].create(to_create)

    def _remove_orphan_packagings(self):
        """Remove the packagings whose UoM is no longer in the template's UoMs."""
        for product in self:
            target_uoms = product.product_tmpl_id.uom_ids
            product.packaging_ids.filtered(
                lambda p, uoms=target_uoms: p.uom_id not in uoms
            ).unlink()

    def _recompute_packagings(self):
        """Sync each variant's packagings with its template's UoMs"""
        self._remove_orphan_packagings()
        self._create_missing_packagings()

    @api.model
    def get_views(self, views, options=None):
        # OVERRIDE to add the uom inline names to the field labels
        self = self.with_context(uom_inline_field_labels=True)
        return super().get_views(views, options)
