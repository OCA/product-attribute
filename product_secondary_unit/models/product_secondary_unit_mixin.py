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
    )
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Second unit",
        ondelete="restrict",
        default=_get_default_secondary_uom,
    )

    def _get_uom_line(self):
        return self[self._secondary_unit_fields["uom_field"]]

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

    def _get_secondary_uom_qty_from_uom_qty(self):
        self.ensure_one()
        factor = self._get_factor_line()
        qty_line = self._get_quantity_from_line()
        return float_round(
            qty_line / (factor or 1.0),
            precision_rounding=self.secondary_uom_id.uom_id.rounding or 0.01,
        )

    @api.depends(lambda x: x._get_secondary_uom_qty_depends())
    def _compute_secondary_uom_qty(self):
        """Compute the secondary qty field defined based on uom qty_field"""
        for line in self:
            if not line.secondary_uom_id:
                line.secondary_uom_qty = 0.0
                continue
            elif line.secondary_uom_id.dependency_type == "independent":
                continue
            line.secondary_uom_qty = line._get_secondary_uom_qty_from_uom_qty()
        # To avoid recompute uom qty_field when secondary_uom_qty changes.
        self.env.remove_to_compute(
            field=self._fields[self._secondary_unit_fields["qty_field"]], records=self
        )

    def _get_default_value_for_qty_field(self):
        return self.default_get([self._secondary_unit_fields["qty_field"]]).get(
            self._secondary_unit_fields["qty_field"]
        )

    def _get_uom_qty_from_secondary_uom_qty(self):
        self.ensure_one()
        factor = self._get_factor_line()
        return float_round(
            self.secondary_uom_qty * factor,
            precision_rounding=self._get_uom_line().rounding,
        )

    def _compute_helper_target_field_qty(self):
        """Set the target qty field defined in model"""
        default_qty_field_value = self._get_default_value_for_qty_field()
        for rec in self.filtered("secondary_uom_id"):
            if rec.secondary_uom_id.dependency_type == "independent":
                if rec[rec._secondary_unit_fields["qty_field"]] == 0.0:
                    rec[
                        rec._secondary_unit_fields["qty_field"]
                    ] = default_qty_field_value
                continue
            # To avoid recompute secondary_uom_qty field when
            # secondary_uom_id changes.
            rec.env.remove_to_compute(
                field=rec._fields["secondary_uom_qty"], records=rec
            )
            rec[
                rec._secondary_unit_fields["qty_field"]
            ] = rec._get_uom_qty_from_secondary_uom_qty()

    def _onchange_helper_product_uom_for_secondary(self):
        """Helper method to be called from onchange method of uom field in
        target model.
        """
        if not self.secondary_uom_id:
            self.secondary_uom_qty = 0.0
            return
        elif self.secondary_uom_id.dependency_type == "independent":
            return
        self.secondary_uom_qty = self._get_secondary_uom_qty_from_uom_qty()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.secondary_uom_id and not self.env.context.get(
            "skip_default_secondary_uom_qty", False
        ):
            defaults["secondary_uom_qty"] = 1.0
        return defaults
