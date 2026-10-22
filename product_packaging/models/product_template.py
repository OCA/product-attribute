# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Edits the single variant's packaging (only meaningful, and only shown,
    # when the template has exactly one variant).
    packaging_ids = fields.One2many(
        comodel_name="product.packaging",
        compute="_compute_packaging_ids",
        readonly=False,
        string="Packaging",
    )
    # Keep ``uom_ids`` as the single source of truth at the UoM level, but
    # derive it from the variants' packagings and reconcile back through them.
    uom_ids = fields.Many2many(
        compute="_compute_uom_ids",
        inverse="_inverse_uom_ids",
        store=True,
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        # ``uom_ids`` and ``packaging_ids`` are materialized into per-variant
        # packagings, which can only be created once the variants exist. On
        # create the variants are built after these values are first processed
        # (``uom_ids`` even gets wiped by its own recompute when no packaging
        # exists yet), so re-apply the requested values now to (re)create them.
        # When ``create_product_product`` is False the template is only being
        # delegated from ``product.product.create`` (the variant doesn't exist
        # yet); that flow re-applies the values itself, so skip it here.
        if self.env.context.get("create_product_product", True):
            for template, vals in zip(templates, vals_list, strict=True):
                if uom_ids := vals.get("uom_ids"):
                    template.uom_ids = uom_ids
                if packaging_ids := vals.get("packaging_ids"):
                    template._write_variant_packagings(packaging_ids)
        return templates

    def write(self, vals):
        packaging_commands = vals.pop("packaging_ids", None)
        res = super().write(vals)
        if packaging_commands is not None:
            for template in self:
                template._write_variant_packagings(packaging_commands)
        return res

    def _write_variant_packagings(self, commands):
        """Forward ``packaging_ids`` commands to the single variant's own field.

        Going through the variant's real One2many applies per-row field updates
        (weight, volume, ...) correctly, which the computed field's recompute
        would otherwise discard.
        """
        self.ensure_one()
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.write({"packaging_ids": commands})

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.packaging_ids",
        "product_variant_ids.packaging_ids.uom_id",
    )
    def _compute_uom_ids(self):
        for template in self:
            template.uom_ids = template.product_variant_ids.packaging_ids.uom_id

    def _inverse_uom_ids(self):
        self.product_variant_ids._recompute_packagings()

    @api.depends("product_variant_ids.packaging_ids")
    def _compute_packaging_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.packaging_ids = template.product_variant_ids.packaging_ids
            else:  # pragma: no cover
                template.packaging_ids = False

    @api.model
    def get_views(self, views, options=None):
        # OVERRIDE to add the uom inline names to the field labels
        self = self.with_context(uom_inline_field_labels=True)
        return super().get_views(views, options)
