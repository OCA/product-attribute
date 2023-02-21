from odoo import api, fields, models

from ..constants import constants


class SaleOrderLine(models.Model):
    """
    SaleOrderLine - add fields
    and compute value from custom dimension in mm
    """

    _inherit = "sale.order.line"

    product_length = fields.Float(
        string="Length", compute="_compute_set_attribute_to_field", store=True
    )
    product_width = fields.Float(
        string="Width", compute="_compute_set_attribute_to_field", store=True
    )

    product_height = fields.Float(
        string="Height", compute="_compute_set_attribute_to_field", store=True
    )
    product_area_wh = fields.Float(
        string="Area", compute="_compute_set_attribute_to_field", store=True
    )
    product_volume = fields.Float(
        string="Volume", compute="_compute_set_attribute_to_field", store=True
    )
    product_weight = fields.Float(
        string="Weight", compute="_compute_set_attribute_to_field", store=True
    )

    configurator_data = fields.Text(
        string="Selected attributes",
        help="Selected attributes in configurator",
    )

    def get_line_dimensions_values(self):
        self.ensure_one()
        line_dimensions: dict = {}
        try:
            # if we create new database, in compute method we can not to use
            # records from xml files. They are still not loaded to db
            dimensions_base_uom_ids = constants.dimensions_base_uom_ids(self.env)
        except ValueError:
            dimensions_base_uom_ids = {}
        pcav = self.product_custom_attribute_value_ids
        for attr in pcav:
            if attr.custom_value:
                attr_cptav_id = attr.custom_product_template_attribute_value_id
                product_attribute_value_id = attr_cptav_id.product_attribute_value_id
                uom_id = product_attribute_value_id.uom_id
                if uom_id:
                    dimension_attr = product_attribute_value_id.attribute_id.dimension
                    if dimension_attr:
                        base_dimension_uom = dimensions_base_uom_ids.get(
                            dimension_attr, False
                        )
                        if product_attribute_value_id.uom_id != base_dimension_uom:
                            line_dimensions.update(
                                {
                                    dimension_attr: uom_id._compute_quantity(
                                        float(attr.custom_value), base_dimension_uom
                                    )
                                }
                            )
                        else:
                            line_dimensions.update(
                                {dimension_attr: float(attr.custom_value)}
                            )
        line_dimensions = constants.check_dim_vals(line_dimensions)
        return line_dimensions

    @api.depends("product_custom_attribute_value_ids")
    def _compute_set_attribute_to_field(self):
        """Compute value dimension in standard value (mm)"""
        for rec in self:
            line_dimensions = rec.get_line_dimensions_values()
            rec.write(line_dimensions)

    @api.onchange("product_id")
    def product_id_change(self):
        dimension_context_params = {
            dimension: getattr(self, dimension, 0.0)
            for dimension in constants.LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT
        }
        result = super(
            SaleOrderLine, self.with_context(**dimension_context_params)
        ).product_id_change()
        return result

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        dimension_context_params = self.get_line_dimensions_values()
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get("fiscal_position"),
                **dimension_context_params
            )
            new_context = dict(self.env.context)
            new_context.update(dimension_context_params)
            new_context.update({"pricelist": self.order_id.pricelist_id.id})
            self = self.with_context(**new_context)
            self.price_unit = product._get_tax_included_unit_price(
                self.company_id,
                self.order_id.currency_id,
                self.order_id.date_order,
                "sale",
                fiscal_position=self.order_id.fiscal_position_id,
                product_price_unit=self._get_display_price(product),
                product_currency=self.order_id.currency_id,
            )
