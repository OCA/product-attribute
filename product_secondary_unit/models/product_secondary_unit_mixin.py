# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class ProductSecondaryUnitMixin(models.AbstractModel):
    """
    Mixin model that allows to compute a field from a secondary unit helper
    An example is to extend any model in which you want to compute quantities
    based on secondary units. You must add a dictionary `_secondary_unit_fields`
    as class variable with the following content:
    _secondary_unit_fields = {
        "qty_field": "product_uom_qty",
        "uom_field": "product_uom"
    }

    To compute ``qty_field`` on target model, you must convert the field to computed
    writable (computed, stored and readonly=False), and you have to define the
    compute method adding ``secondary_uom_id`` and ``secondary_uom_qty`` fields
    as dependencies and calling inside to ``self._compute_helper_target_field_qty()``.

    To compute secondary units when user changes the uom field on target model,
    you must add an onchange method on uom field and call to
    ``self._onchange_helper_product_uom_for_secondary()``

    You can see an example in ``purchase_order_secondary_unit`` on purchase-workflow
    repository.
    """

    _name = "product.secondary.unit.mixin"
    _description = "Product Secondary Unit Mixin"
    _secondary_unit_fields = {}
    _product_uom_field = "uom_id"

    @api.model
    def _get_default_secondary_uom(self):
        return self.env["product.template"]._get_default_secondary_uom()

    secondary_uom_qty = fields.Float(
        string="Secondary Qty",
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
        compute="_compute_secondary_uom_qty",
        precompute=True,
    )
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Second unit",
        ondelete="restrict",
        default=lambda self: self._get_default_secondary_uom(),
    )

    def _get_uom_line(self):
        return self[self._secondary_unit_fields["uom_field"]]

    # TODO: This method is now not used in this module. Deprecate it in future.
    def _get_factor_line(self):
        uom_line = self._get_uom_line()
        return self.secondary_uom_id.factor * (
            uom_line.factor
            if self.product_id[self._product_uom_field] != uom_line
            else 1.0
        )

    def _get_quantity_from_line(self):
        return self[self._secondary_unit_fields["qty_field"]]

    @api.model
    def _get_secondary_uom_qty_depends(self):
        if not self._secondary_unit_fields:
            return []
        return [self._secondary_unit_fields["qty_field"]]

    @api.model
    def _convert_qty_to_secondary_uom(self, qty):
        # Intended to be called from other operations if needed.
        self.ensure_one()
        uom_line = self._get_uom_line()
        uom_product = self.product_id[self._product_uom_field]
        if uom_line != uom_product:
            qty = uom_line._compute_quantity(qty, uom_product)
        return float_round(
            qty / (self.secondary_uom_id.factor or 1.0),
            precision_rounding=self.secondary_uom_id.uom_id.rounding,
        )

    @api.depends(lambda x: x._get_secondary_uom_qty_depends())
    def _compute_secondary_uom_qty(self):
        for line in self:
            if not line.secondary_uom_id:
                line.secondary_uom_qty = 0.0
                continue
            elif line.secondary_uom_id.dependency_type == "independent":
                continue
            qty_line = line._get_quantity_from_line()
            line.secondary_uom_qty = line._convert_qty_to_secondary_uom(qty_line)

    def _get_default_value_for_qty_field(self):
        return self.default_get([self._secondary_unit_fields["qty_field"]]).get(
            self._secondary_unit_fields["qty_field"]
        )

    def _compute_helper_target_field_qty(self):
        """Set the target qty field defined in model"""
        default_qty_field_value = self._get_default_value_for_qty_field()
        for rec in self:
            if not rec.secondary_uom_id:
                rec[rec._secondary_unit_fields["qty_field"]] = (
                    rec[rec._secondary_unit_fields["qty_field"]]
                    or default_qty_field_value
                )
                continue
            if rec.secondary_uom_id.dependency_type == "independent":
                if rec[rec._secondary_unit_fields["qty_field"]] == 0.0:
                    rec[rec._secondary_unit_fields["qty_field"]] = (
                        default_qty_field_value
                    )
                continue
            # To avoid recompute secondary_uom_qty field when
            # secondary_uom_id changes.
            rec.env.remove_to_compute(
                field=rec._fields["secondary_uom_qty"], records=rec
            )
            qty_base = rec.secondary_uom_qty * rec.secondary_uom_id.factor
            uom_line = rec._get_uom_line()
            uom_product = rec.product_id[rec._product_uom_field]
            qty_line = uom_product._compute_quantity(qty_base, uom_line)
            rec[rec._secondary_unit_fields["qty_field"]] = qty_line

    def _onchange_helper_product_uom_for_secondary(self):
        """Helper method to be called from onchange method of uom field in
        target model.
        """
        if not self.secondary_uom_id:
            self.secondary_uom_qty = 0.0
            return
        elif self.secondary_uom_id.dependency_type == "independent":
            return
        qty_line = self._get_quantity_from_line()
        self.secondary_uom_qty = self._convert_qty_to_secondary_uom(qty_line)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.secondary_uom_id and not self.env.context.get(
            "skip_default_secondary_uom_qty", False
        ):
            defaults["secondary_uom_qty"] = 1.0
        return defaults
