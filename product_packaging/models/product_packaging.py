# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _name = "product.packaging"
    _description = "Product Packaging"
    _order = "product_tmpl_id, product_id, sequence, uom_id"
    _rec_name = "uom_id"

    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        ondelete="cascade",
        index=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        related="product_id.product_tmpl_id",
        store=True,
        index=True,
    )
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Packaging",
        required=True,
        ondelete="cascade",
        domain="[('id', '!=', product_uom_id)]",
        index=True,
    )
    sequence = fields.Integer(default=10)
    qty = fields.Float(
        string="Quantity",
        compute="_compute_qty",
        digits="Product Unit",
        help="How many product base units this packaging contains.",
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        related="product_id.uom_id",
        string="Unit",
    )
    weight = fields.Float(
        compute="_compute_weight",
        store=True,
        readonly=False,
        digits="Stock Weight",
    )
    weight_uom_name = fields.Char(related="product_id.weight_uom_name")
    volume = fields.Float(
        compute="_compute_volume",
        store=True,
        readonly=False,
        digits="Volume",
    )
    volume_uom_name = fields.Char(related="product_id.volume_uom_name")
    barcode_ids = fields.One2many(
        string="Barcodes",
        comodel_name="product.uom",
        inverse_name="packaging_id",
        domain="[('product_id', '=', product_id), ('uom_id', '=', uom_id)]",
    )

    _product_packaging_unique = models.Constraint(
        "UNIQUE (product_id, uom_id)",
        "A packaging unit can only be defined once per product.",
    )
    _positive_weight = models.Constraint(
        "CHECK(weight>=0)",
        "Weight must be positive",
    )
    _positive_volume = models.Constraint(
        "CHECK(volume>=0)",
        "Volume must be positive",
    )

    @api.depends("uom_id", "product_id.uom_id")
    def _compute_qty(self):
        for packaging in self:
            packaging.qty = packaging.uom_id._compute_quantity(
                1.0, packaging.product_id.uom_id, round=False, raise_if_failure=False
            )

    @api.depends("product_id.uom_id", "uom_id.factor")
    def _compute_weight(self):
        for packaging in self:
            packaging.weight = packaging.product_id.weight * packaging.qty

    @api.depends("product_id.uom_id", "uom_id.factor")
    def _compute_volume(self):
        for packaging in self:
            packaging.volume = packaging.product_id.volume * packaging.qty

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # OVERRIDE to add the uom to the field label
        res = super().fields_get(allfields, attributes)
        if self.env.context.get("uom_inline_field_labels"):
            ProductTemplate = self.env["product.template"]
            if "weight" in res and "string" in res["weight"]:
                weight_uom_name = (
                    ProductTemplate._get_weight_uom_name_from_ir_config_parameter()
                )
                res["weight"]["string"] += f" ({weight_uom_name})"
            if "volume" in res and "string" in res["volume"]:
                volume_uom_name = (
                    ProductTemplate._get_volume_uom_name_from_ir_config_parameter()
                )
                res["volume"]["string"] += f" ({volume_uom_name})"
        return res

    def get_view(self, view_id=None, view_type="form", **options):
        # OVERRIDE to add the uom inline names to the field labels
        if view_type == "list":
            self = self.with_context(uom_inline_field_labels=True)
        return super().get_view(view_id, view_type=view_type, **options)
