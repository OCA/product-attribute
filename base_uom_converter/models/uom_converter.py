# Copyright <2021> <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class UomConverter(models.Model):
    _name = "uom.converter"
    _description = "UoM converter"

    _sql_constraints = [("unique_name", "unique (name)", "This name already exists")]

    name = fields.Char(string="Scale", required=True, index=True)
    from_uom_id = fields.Many2one(
        "uom.uom",
        "Source Unit of Measure",
        required=True,
        help="Source unit of measure, while converting a quantity it "
        "must be in this UoM to get the right scale. Or in a unit in the "
        "same category that would be convert before getting the right line.",
    )
    to_uom_id = fields.Many2one(
        "uom.uom",
        "Destinaiton Unit of Measure",
        required=True,
        help="Destination unit of measure, while converting a quantity result "
        "will be in this UoM. Or in a unit in the same category that would be "
        "convert after getting the new quantity.",
    )
    line_ids = fields.One2many(
        "uom.converter.line",
        "uom_converter_id",
        "UoM converter lines",
    )

    def convert(self, quantity, uom_qty=None, result_uom=None):
        """Return quantity in to_uom_id or result_uom if set and in the same
        uom category.

        Given quantity is used to select the right scale line. if uom_qty is set
        and different from the `self.from_uom_id` quantity it is converted
        before scale line selection as long they share the same uom_category.
        """
        self.ensure_one()
        if not uom_qty:
            uom_qty = self.from_uom_id
        else:
            if uom_qty.category_id.id != self.from_uom_id.category_id.id:
                raise ValidationError(
                    _(
                        "You can't convert {uom} (expected {category} uom "
                        "category) to {to_uom} using this converter {converter}."
                    ).format(
                        uom=uom_qty.name,
                        category=self.from_uom_id.category_id.name,
                        to_uom=self.to_uom_id.name,
                        converter=self.name,
                    )
                )
            if uom_qty.id != self.from_uom_id.id:
                quantity = uom_qty._compute_quantity(
                    quantity,
                    self.from_uom_id,
                )
        if not result_uom:
            result_uom = self.to_uom_id
        else:
            if result_uom.category_id.id != self.to_uom_id.category_id.id:
                raise ValidationError(
                    _(
                        "You can't convert {uom} to {to_uom} (expect "
                        "{expected_category} unit category) using this "
                        "converter {converter}."
                    ).format(
                        uom=uom_qty.name,
                        to_uom=result_uom.name,
                        expected_category=self.to_uom_id.category_id.name,
                        converter=self.name,
                    )
                )
        convert_line = self.line_ids.search(
            [("uom_converter_id", "=", self.id), ("max_qty", ">=", quantity)],
            order="max_qty",
            limit=1,
        )
        if len(convert_line) == 0:
            raise ValidationError(
                _(
                    "You can't converter {quantity} {uom} to {to_uom} using "
                    "this converter {converter}. This quantity is out of "
                    "configured scale."
                ).format(
                    quantity=quantity,
                    uom=uom_qty.name,
                    to_uom=result_uom.name,
                    converter=self.name,
                )
            )

        result = quantity * convert_line.coefficient + convert_line.constant
        if result_uom.id != self.to_uom_id.id:
            result = self.to_uom_id._compute_quantity(result, result_uom)
        return result


class UomConverterLine(models.Model):
    _name = "uom.converter.line"
    _description = "UoM converter scale line"
    _order = "uom_converter_id, max_qty"

    uom_converter_id = fields.Many2one(
        "uom.converter",
        string="Converter",
        required=True,
        ondelete="cascade",
        help="UoM converter this line is related to",
    )
    max_qty = fields.Float(
        string="Maximum",
        required=True,
        digits=(16, 4),
        help="Maximum quantity in the Source Unit of Measure of the current "
        "converter (`from_uom_id` field). If qty is higher to this value while "
        "converting quantity this line will be ignored",
    )
    coefficient = fields.Float(
        string="Coefficient",
        digits=(16, 4),
        help=(
            "Coefficient to apply on the converted quantity (To UoM / From UoM). "
            "Result Qty = converted quantity * coefficient + constant"
        ),
    )
    constant = fields.Float(
        string="Constant",
        digits=(16, 4),
        help=(
            "Constant to add to the result quantity (To UoM). Result Qty = "
            "converted quantity * coefficient + constant"
        ),
    )
