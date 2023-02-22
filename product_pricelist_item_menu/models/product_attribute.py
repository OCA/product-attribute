from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_round

from ..constants import constants


#####################
# Product Attribute #
#####################
class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    active = fields.Boolean(string="Active", default=1)
    dimension = fields.Selection(
        string="Dimension",
        selection=constants.DIMENSION_SELECTION,
    )

    @api.onchange("dimension")
    def check_dimension_selection(self):
        if not self.dimension:
            self.update(
                {
                    "create_variant": "no_variant",
                    "display_type": "radio",
                }
            )

    def write(self, vals):
        """
        Fix for updating demo data
        """
        if "create_variant" in vals and "demo" in vals:
            vals.pop("create_variant", None)
            vals.pop("demo", None)
        res = super(ProductAttribute, self).write(vals)
        return res


####################################
# Product Template Attribute Value
####################################
class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    dimension_rule_ids = fields.Many2many(
        string="Dimension Exclusion Rules",
        comodel_name="ooops.dimension.exclusion.rule",
        compute="_compute_dimension_exclusion_rule_ids",
    )

    price_extra = fields.Float(
        compute="_compute_price_extra",
    )
    price_extra_storable = fields.Float(string="price_extra")
    price_extra_base = fields.Float(
        string="Attribute Extra Price",
        digits="Product Price",
        help="Base for attribute extra price",
    )

    price_type = fields.Selection(
        string="Dimension",
        selection=constants.PRICE_TYPE_SELECTION,
        default=constants.FIXED_PRICE_TYPE,
        copy=False,
        required=True,
    )

    uom_category_price_type = fields.Many2one(
        string="Uom Category",
        help="Uom Category",
        comodel_name="uom.category",
        compute="_compute_uom_category_price_type",
    )

    price_extra_base_uom = fields.Float(
        string="Attribute Extra Price ",
        digits="Product Price",
        help="Base for attribute extra price",
    )

    using_uom = fields.Many2one(
        string="UOM",
        help="Using uom",
        comodel_name="uom.uom",
    )

    price_surcharge = fields.Float(
        string="Price Surcharge",
        digits="Product Price",
        help="Specify the fixed amount to add"
        " or subtract(if negative) to the amount calculated with the discount.",
    )
    price_round = fields.Float(
        string="Price Rounding",
        digits="Product Price",
        help="Sets the price so that it is a multiple of this value.\n"
        "Rounding is applied after the discount and before the surcharge.\n"
        "To have prices that end in 9.99, set rounding 10, surcharge -0.01",
    )
    value_raise_up = fields.Float(
        string="Raise Value Up To ",
        help="Rise all dimensional values below this value up to this value",
    )
    uom_value_raise_up = fields.Float(
        string="Raise Value Up To",
        help="Rise all dimensional values below this value up to this value",
    )
    price_formula = fields.Char(string="Extra Price", compute="_compute_price_formula")

    related_extra_price_dimension = fields.Selection(
        string="Related Product (for Extra Price) Dimension",
        selection=constants.PRICE_TYPE_SELECTION,
        copy=False,
    )

    extra_price_product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Related Product (for Extra Price)",
    )

    price_extra_manual = fields.Float(
        string="Attribute Price Extra ",
        default=0.0,
        digits="Product Price",
    )

    price_extra = fields.Float(
        string="Attribute Price Extra",
        default=0.0,
        digits="Product Price",
        help="Price Extra: Extra price for the variant with "
        "this attribute value on sale price. eg. 200 price extra, "
        "1000 + 200 = 1200. "
        'If "Related Product (for Extra Price)" is set its taken '
        "from that product sales price. ",
        compute="_compute_price_extra",
        inverse="_inverse_price_extra",
    )

    def _inverse_price_extra(self):
        for rec in self:
            rec.price_extra_manual = rec.price_extra

    @api.depends(
        "extra_price_product_tmpl_id",
        "extra_price_product_tmpl_id.list_price",
        "price_extra_manual",
    )
    @api.onchange(
        "price_extra_base_uom",
        "using_uom",
        "price_type",
        "uom_value_raise_up",
        "extra_price_product_tmpl_id",
    )
    def _compute_price_extra_base(self):
        for record in self:
            record._compute_uom_category_price_type()
            record.set_price_type_to_fixed()
            values_for_record = record._get_price_extra_base_values_for_record()
            if record.price_type == "f":
                values_for_record["using_uom"] = False
                values_for_record["uom_value_raise_up"] = 0
            record._origin.update(values_for_record)
            record.update(values_for_record)

    def _get_price_extra_base_values_for_record(self):
        self.ensure_one()
        values = {}
        values["price_extra_base"] = self.price_extra_base_uom
        if self.price_type and self.price_type != constants.FIXED_PRICE_TYPE:
            base_uom = self.env.ref(constants.DIMENSIONS_BASE_UOM[self.price_type])
            if base_uom.category_id.id == self.using_uom.category_id.id:
                values["using_uom"] = self.using_uom
            else:
                values["using_uom"] = base_uom
        return values

    def _compute_uom_category_price_type(self):
        for record in self:
            record.uom_category_price_type = False
            if record.price_type and record.price_type != constants.FIXED_PRICE_TYPE:
                base_uom = record.env.ref(
                    constants.DIMENSIONS_BASE_UOM[record.price_type]
                )
                record.uom_category_price_type = base_uom.category_id.id

    @api.depends("product_tmpl_id", "product_attribute_value_id")
    def _compute_dimension_exclusion_rule_ids(self):
        """
        Compute dimension exclusion rules for current product template
        :return: None
        """

        der_all_ids = self.env["ooops.dimension.exclusion.rule"].search([])
        for record in self:
            current_der_ids = self.env["ooops.dimension.exclusion.rule"]
            for der in der_all_ids:
                for ptav_id in der.product_tmpl_ids:
                    if ptav_id.id == record.product_tmpl_id.id:
                        for value_id in der.value_ids:
                            if value_id.id == record.product_attribute_value_id.id:
                                current_der_ids = current_der_ids + der
            record.update({"dimension_rule_ids": [(6, 0, current_der_ids.ids)]})

    # -- Compute price formula
    def _compute_price_formula(self):
        """
        Computes char representation of price formula
        :return:
        """
        for rec in self:
            price_type = rec.price_type
            if not price_type or price_type == constants.FIXED_PRICE_TYPE:
                rec.update({"price_formula": str(rec.price_extra_base)})
            else:
                rec.update(
                    {
                        "price_formula": "{price_extra_base}{uom} * {price_type} + "
                        "({price_surcharge})".format(
                            price_extra_base=rec.price_extra_base_uom,
                            price_type=rec.price_type,
                            price_surcharge=rec.price_surcharge,
                            uom=rec.using_uom.name or "",
                        ),
                    }
                )

    def _get_dim_vals(self):
        # Get dimensional UOM's
        dim_vals = {}
        # Default UOM is millimeters
        for rec in self:
            uom_id = rec.product_attribute_value_id.uom_id
            if uom_id:
                dimension = rec.attribute_id.dimension
                if dimension:
                    context_dim_value = self.env.context.get(dimension, False)
                    if not context_dim_value:
                        context_dim_value = self.env.context.get("dim_vals", {}).get(
                            dimension, 0
                        )
                    if context_dim_value == "":
                        context_dim_value = 0
                    dim_value = uom_id._compute_quantity(
                        float(context_dim_value),
                        self.env.ref(constants.DIMENSIONS_BASE_UOM[dimension]),
                    )
                    dim_vals.update({dimension: dim_value})
        # Check if data are in context
        if not dim_vals:
            dim_vals = self.env.context.get("dim_vals", False)
            if not dim_vals:
                dim_vals = {
                    dimension: self.env.context.get(dimension, 0)
                    for dimension in constants.LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT
                }
        dim_vals = constants.check_dim_vals(dim_vals)
        return dim_vals

    @api.depends(
        "extra_price_product_tmpl_id",
        "extra_price_product_tmpl_id.list_price",
        "price_extra_manual",
    )
    def _compute_price_extra(self):
        """
        !!! IMPORTANT !!!
        This method is completely redefined in module
        ooops_configurator_attribute_product_link_dimensions.
        When updating it make sure it is updated there accordingly!
        """
        for rec in self:
            if rec.price_extra_storable:
                rec.update({"price_extra": rec.price_extra_storable})

            price_extra = rec.with_context(
                **self.env.context
            )._compute_price_extra_for_record()
            rec.update({"price_extra": price_extra})

            if rec.extra_price_product_tmpl_id:
                if self.env.context.get("pricelist"):
                    rec.price_extra = rec.extra_price_product_tmpl_id.price
                else:
                    rec.price_extra = rec.extra_price_product_tmpl_id.list_price
            else:
                rec.price_extra = rec.price_extra_manual

    def set_price_type_to_fixed(self):
        if not self.extra_price_product_tmpl_id:
            self.price_type = "f"

    def get_related_product_tmpl_id(self):
        self.ensure_one()
        dim_vals = self._get_dim_vals()
        return self.extra_price_product_tmpl_id.with_context(**dim_vals)

    def get_pricelist(self):
        self.ensure_one()
        pricelist_id = self.env.context.get("pricelist", False)
        pricelist = self.env["product.pricelist"]

        if pricelist_id:
            pricelist = pricelist.search(
                [
                    ("id", "=", pricelist_id),
                ]
            )
        return pricelist

    def get_selected_dimension_value(self):
        self.ensure_one()
        dim_vals = self._get_dim_vals()
        sel_dim = self.get_selected_dimension()
        dim_value = dim_vals.get(sel_dim, 0)
        return dim_value

    def get_selected_dimension_value_for_selected_uom(self):
        self.ensure_one()
        dim_vals = self._get_dim_vals()
        sel_dim = self.get_selected_dimension()
        dim_value = dim_vals.get(sel_dim, 0)
        base_uom = self.get_base_uom()
        using_uom_quantity = self.using_uom._compute_quantity(1, base_uom)  # noqa
        dim_value = dim_value / using_uom_quantity
        return dim_value

    def get_pricelist_items(self):
        self.ensure_one()
        ptav_record = self
        related_product_tmpl_id = ptav_record.get_related_product_tmpl_id()
        pricelist = ptav_record.get_pricelist()
        linked_pricelist_items_to_check = self.env["product.pricelist.item"]
        final_pricelists = self.env["product.pricelist"]
        pricelist_items = self.env["product.pricelist.item"]
        if related_product_tmpl_id and pricelist:
            products = self.env["product.product"].search(
                [("product_tmpl_id", "=", related_product_tmpl_id.id)]
            )
            pricelist_items = pricelist.with_context(
                **ptav_record._get_dim_vals()
            )._compute_price_rule_get_items(
                products_qty_partner=None,
                date=fields.Datetime.now(),
                uom_id=None,
                prod_tmpl_ids=related_product_tmpl_id.ids,
                prod_ids=products.ids,
                categ_ids=related_product_tmpl_id.categ_id.ids,
            )
            if pricelist_items.base == "pricelist":
                linked_pricelist = pricelist_items.base_pricelist_id
                linked_pricelist_items_to_check = linked_pricelist.with_context(
                    **ptav_record._get_dim_vals()
                )._compute_price_rule_get_items(
                    products_qty_partner=None,
                    date=fields.Datetime.now(),
                    uom_id=None,
                    prod_tmpl_ids=related_product_tmpl_id.ids,
                    prod_ids=products.ids,
                    categ_ids=related_product_tmpl_id.categ_id.ids,
                )
            final_pricelists = final_pricelists | pricelist
        return pricelist_items, final_pricelists, linked_pricelist_items_to_check

    def get_base_price(self):
        # REQUIRED BEHAVIOR
        # if the pricelist line applied has compute price = fixed, display value of
        # field "Fixed Price";
        # if the pricelist line applied has "compute price = formula,
        # based on = other pricelist" AND the applied line has "compute price = fixed",
        # display value of field "Fixed Price" from the pricelist line on the "other pricelist"
        self.ensure_one()
        base_price = self.price_extra_base_uom
        with_rel_prod = self.get_related_product_tmpl_id()
        if with_rel_prod:
            base_price = self.get_related_product_tmpl_id().list_price
            pricelist_items = self.get_pricelist_items()[0]
            linked_pricelist_items_to_check = self.get_pricelist_items()[2]
            if pricelist_items.compute_price == "fixed":
                base_price = pricelist_items[0].fixed_price
            if linked_pricelist_items_to_check:
                if pricelist_items.compute_price == "formula":
                    if linked_pricelist_items_to_check.compute_price == "fixed":
                        base_price = linked_pricelist_items_to_check.fixed_price
        return base_price

    def get_standart_price(self):
        base_price = self.get_base_price()
        standart_price = base_price
        billing_minimum = self.get_billing_minimum()
        dim_val = self.get_selected_dimension_value_for_selected_uom()
        if self.check_for_dimvals_usage() and dim_val >= billing_minimum:
            standart_price = dim_val * base_price
        elif self.check_for_dimvals_usage() and dim_val < billing_minimum:
            standart_price = billing_minimum * base_price
        return standart_price

    def check_for_dimvals_usage(self):
        self.ensure_one()
        selected_dimension = self.get_selected_dimension()
        return not selected_dimension == constants.FIXED_PRICE_TYPE

    def get_selected_dimension(self):
        self.ensure_one()
        return self.price_type

    def get_selected_uom(self):
        self.ensure_one()
        return self.using_uom

    def get_selected_dimension_with_uom(self):
        self.ensure_one()
        selected_dimension = self.get_selected_dimension()
        selected_uom = self.get_selected_uom()
        if selected_dimension != constants.FIXED_PRICE_TYPE:
            return "%s %s" % (
                dict(constants.PRICE_TYPE_SELECTION)[selected_dimension],
                selected_uom.name,
            )
        elif selected_dimension == constants.FIXED_PRICE_TYPE:
            return dict(constants.PRICE_TYPE_SELECTION)[selected_dimension]
        else:
            return ""

    def get_billing_minimum(self):
        self.ensure_one()
        billing_minimum = 0.0
        if self.uom_value_raise_up:
            billing_minimum = self.uom_value_raise_up
        return billing_minimum

    def get_base_uom(self):
        self.ensure_one()
        base_uom = self.env["uom.uom"]
        if self.check_for_dimvals_usage():
            sel_dim = self.get_selected_dimension()
            base_uom = self.env.ref(constants.DIMENSIONS_BASE_UOM[sel_dim])
        return base_uom

    def get_final_price(self):
        self.ensure_one()
        with_rel_prod = self.get_related_product_tmpl_id()
        base_price = self.get_base_price()
        pricelist = self.get_pricelist()
        if with_rel_prod and pricelist:
            base_price = self.get_related_product_tmpl_id().price

        final_price = base_price
        billing_minimum = self.get_billing_minimum()
        dim_val = self.get_selected_dimension_value_for_selected_uom()
        if self.check_for_dimvals_usage() and dim_val >= billing_minimum:
            final_price = dim_val * final_price

        elif self.check_for_dimvals_usage() and dim_val < billing_minimum:
            final_price = billing_minimum * final_price
        if not with_rel_prod:
            final_price += self.price_surcharge
            if self.price_round:
                final_price = float_round(
                    final_price, precision_rounding=self.price_round
                )
        return final_price

    def get_price_extra(self):
        self.ensure_one()
        price_extra = self.get_final_price()
        return price_extra

    def get_currency(self):
        self.ensure_one()
        currency = self.env.company.currency_id
        rel_product_tmpl = self.get_related_product_tmpl_id()
        if rel_product_tmpl:
            currency = rel_product_tmpl.currency_id
            pricelist = self.get_pricelist()
            if pricelist:
                currency = pricelist.currency_id
        return currency

    def get_final_price_with_currency(self):
        self.ensure_one()
        final_price = self.get_final_price()
        currency = self.get_currency()
        return "%s %s" % (currency.symbol, final_price)

    def _compute_price_extra_for_record(self):
        self.ensure_one()
        return self.get_price_extra()

    # -- Compute dimension price
    @api.model
    def _dimensions_allowed(self, dimensions):
        """
        Compute extra price based on product dimensions
        :type dict{"dimension": value} dimensions: Dict of dimensional values
         (e.g. {"product_length":102.2}
        """
        for rec in self:
            for rule in rec.dimension_rule_ids:
                allow_with_rule = self.check_dimension_rule(dimensions, rule)
                if not allow_with_rule:
                    return False
        return True

    def check_dimension_rule(self, dimensions, rule):
        """
        Check if dimension is match for current rule
        :param dimensions: dict of dimension
        :param rule: record of rule to check
        :return:
        """
        rule_matched = True
        for line in rule.line_ids:
            is_matched = constants.match_value(
                dimensions[line.dimension], line.value_from, line.value_to
            )
            if not is_matched:
                rule_matched = False
        if rule_matched:
            return False
        return True

    @api.constrains("extra_price_product_tmpl_id", "related_extra_price_dimension")
    def _check_no_dimensions_if_empty_product(self):
        for rec in self:
            if (
                not rec.extra_price_product_tmpl_id
                and rec.related_extra_price_dimension
            ):
                raise UserError(
                    _(
                        'Field "Related Product (for Extra Price) Dimension" '
                        'can only be used together with field "Related Product '
                        '(for Extra Price)."'
                    )
                )

    @api.model
    def create(self, values):
        price_extra = values.get("price_extra", False)
        if price_extra:
            values["price_extra_storable"] = price_extra
        res = super(ProductTemplateAttributeValue, self).create(values)
        return res

    def write(self, values):
        price_extra = values.get("price_extra", False)
        if price_extra:
            values["price_extra_storable"] = price_extra
        res = super(ProductTemplateAttributeValue, self).write(values)
        return res


###########################
# Product Attribute Value #
###########################
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    # -- Domain for UOM
    def _get_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]

    uom_id = fields.Many2one(string="UOM", comodel_name="uom.uom", domain=_get_domain)

    @api.onchange("uom_id")
    def check_uom_selection(self):
        vals = {}
        if not self.name:
            vals["name"] = self.uom_id.name
        self.update(vals)

    # -- Check if attribute value holds dimension
    def is_dimension(self):
        """
        Assumes self is a singleton
        :return: dimension "product_length",
        "product_width" or "product_height" else False
        """
        if self.uom_id and self.attribute_id.dimension:
            return self.attribute_id.dimension
        else:
            return False
