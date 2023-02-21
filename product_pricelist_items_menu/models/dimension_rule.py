from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons import decimal_precision as dp  # noqa

from ..constants import constants

##################
# Dimension Rule #
##################

# ********* GLOSSARY *********

# DEL = Dimension Exclusion Line
# DER = Dimension Exclusion Rule
# PTAV = Product Template Attribute Value
# PT = Product Template


def sanitize_float(val):
    """
    Convert float val to str
    :param float val:
    :return: str
    """
    return str(val).replace(" ", "").replace(".", "-").replace(",", "-")


class DimensionRule(models.Model):
    _name = "ooops.dimension.rule"
    _description = "Dimension Rule"
    _order = "priority"

    name = fields.Text(
        string="Name",
        compute="_compute_name",
        store=True,
    )
    global_id = fields.Char(
        string="Custom ID",
        compute="_compute_global_id",
        store=True,
        index=True,
        help="Used as unique rule identifier",
    )
    priority = fields.Integer(string="Priority")
    product_tmpl_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
        auto_join=True,
        ondelete="cascade",
    )
    product_tmpl_attribute_value_id = fields.Many2one(
        string="Product Template Attribute Value",
        comodel_name="product.template.attribute.value",
        auto_join=True,
        help="If set rule is used for dimension exclusions",
        ondelete="cascade",
    )
    line_ids = fields.One2many(
        string="Lines",
        required=True,
        auto_join=True,
        copy=True,
        comodel_name="ooops.dimension.rule.line",
        inverse_name="rule_id",
    )
    price_extra = fields.Float(
        string="Extra Price", default=0.0, digits="Product Price"
    )
    price_type = fields.Selection(
        string="Dimension",
        selection=constants.PRICE_TYPE_SELECTION,
        default=constants.FIXED_PRICE_TYPE,
        copy=False,
        required=True,
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
    price_type_name = fields.Char(
        string="Price Type", compute="_compute_price_type_name"
    )

    # -- Constraints
    @api.constrains("line_ids", "price_extra")
    def check_constraints(self):
        for rec in self:
            if len(rec.line_ids) < 1:
                raise ValidationError(_("Please add at least one condition!"))
            if (
                rec.product_tmpl_id
                and not rec.product_tmpl_attribute_value_id
                and (not rec.price_extra or rec.price_extra == 0)
            ):
                raise ValidationError(_("Extra price cannot be equal to zero!"))

    # -- Ensure product template is in vals in case it is required
    def _ensure_product_template(self, vals):
        if not vals.get("product_tmpl_id"):
            product_tmpl_attribute_value_id = vals.get(
                "product_tmpl_attribute_value_id"
            )
            if product_tmpl_attribute_value_id:
                product_tmpl_attribute_value = self.env[
                    "product.template.attribute.value"
                ].browse(product_tmpl_attribute_value_id)
                vals.update(
                    {"product_tmpl_id": product_tmpl_attribute_value.product_tmpl_id.id}
                )
        return

    # -- Update existing rules
    @api.model
    def fix_rules(self):
        rules_to_fix = self.sudo().search(
            [
                ("product_tmpl_id", "=", False),
                ("product_tmpl_attribute_value_id", "!=", False),
            ]
        )
        if rules_to_fix:
            for rule in rules_to_fix:
                rule.sudo().write(
                    {
                        "product_tmpl_id": rule.product_tmpl_attribute_value_id.product_tmpl_id.id  # noqa
                    }
                )

    # -- Assign DEL to dimension rule
    @api.model
    def assign_del(self, rule):
        del_obj = (
            self.env["ooops.dimension.exclusion.line"]
            .sudo()
            .with_context(assign_del=True)
        )
        del_id = del_obj.search(
            [
                # ("product_tmpl_id", "=", rule.product_tmpl_id.id),
                ("global_id", "=", rule.global_id),
            ]
        )
        if not del_id:
            # Create new DEL
            del_id = del_obj.create(
                {
                    "product_tmpl_id": [(6, 0, [rule.product_tmpl_id.id])],
                    "value_ids": [(4, rule.product_tmpl_attribute_value_id.id)],
                }
            )

        else:
            # Add PTAV to DEL
            del_id.write({"value_ids": [(4, rule.product_tmpl_attribute_value_id.id)]})
        # Assign DEL to DER
        rule.del_id = del_id.id  # Assign DEL found

    # -- Perform Dimension Exclusion Line operations
    def handle_del(self, operation="create", old_del_dict=None):
        """
        Handle Dimension Exclusion Line operation
        Check UML for details
        :param Char operation: operation performed on rule (create, update, unlink)
        :param Dict old_del_dict: Existing DEL dict
        """
        del_obj = self.env["ooops.dimension.exclusion.line"].sudo()
        # Create
        if operation == "create":
            for rec in self:
                self.assign_del(rec)
        # Write
        elif operation == "write":
            for rec in self:
                self.assign_del(rec)
                del_old = old_del_dict.get(rec.id, False)
                # Remove DER from DEL
                if del_old:
                    del_old.with_context(assign_del=True).write(
                        {"value_ids": [(3, rec.product_tmpl_attribute_value_id.id)]}
                    )
                    # Add DEL to list of empty DELs
                    if len(del_old.rule_ids) == 0:
                        del_obj |= del_old
            # Unlink all empty DELs
            if len(del_obj) > 0:
                del_obj.unlink()
        # Unlink
        elif operation == "unlink":
            for rec in self:
                del_old = old_del_dict.get(rec.id, False)
                # Remove DER from DEL
                if del_old:
                    del_old.with_context(assign_del=True).write(
                        {"value_ids": [(3, rec.product_tmpl_attribute_value_id.id)]}
                    )
                    # Add DEL to list of empty DELs
                    if len(del_old.rule_ids) == 0:
                        del_obj |= del_old

            # Unlink all empty DELs
            if len(del_obj) > 0:
                del_obj.unlink()

    # -- Create
    @api.model
    def create(self, vals):
        self._ensure_product_template(vals)
        if "demo" in vals:
            vals.pop("demo", None)
            return super(DimensionRule, self).create(vals)
        res = super(DimensionRule, self).create(vals)
        if not self._context.get("skip_del", False):
            res.handle_del()
        return res

    # -- Write
    def write(self, vals):
        self._ensure_product_template(vals)
        if "demo" in vals:
            vals.pop("demo", None)
            return super(DimensionRule, self).write(vals)
        if self._context.get("skip_del", False):
            return super(DimensionRule, self).write(vals)

        if "line_ids" in vals:
            old_del_dict = {rec.id: rec.del_id for rec in self}
        else:
            old_del_dict = False
        res = super(DimensionRule, self).write(vals)
        if old_del_dict:
            self.handle_del(operation="write", old_del_dict=old_del_dict)
        self.fix_rules()
        return res

    # -- Unlink
    def unlink(self):
        # Store existing DEL to unlink empty ones later
        del_ids = self.mapped("del_id")
        if not self._context.get("skip_del", False):
            old_del_dict = {rec.id: rec.del_id for rec in self}
            self.handle_del(operation="unlink", old_del_dict=old_del_dict)
        res = super(DimensionRule, self).unlink()
        del_unlink = del_ids.filtered(lambda l: len(l.rule_ids) == 0)
        if len(del_unlink) > 0:
            del_unlink.unlink()
        return res

    # -- Get global id
    @api.model
    def get_global_id(self, rule):
        """
        Returns global id of the rule based on rule values
        :param ooops.dimension.rule rule: Rule object
        :return: char rule ID
        """
        if rule:
            id_parts = []
            for line in rule.line_ids:
                line_part = "_".join(
                    (
                        line.dimension,
                        sanitize_float(line.value_from) if line.value_from else "0",
                        sanitize_float(line.value_to) if line.value_to else "0",
                    )
                )
                id_parts.append(line_part)
            return "_".join(id_parts)
        else:
            return False

    # -- Compose name
    @api.depends("line_ids.name")
    def _compute_name(self):
        for rec in self:
            if len(rec.line_ids) == 1:
                rec.name = rec.line_ids[0].name
            else:
                rec.name = "\nAND ".join([line.name for line in rec.line_ids])

    def _compute_price_type_name(self):
        for rec in self:
            price_type = rec.price_type
            if price_type == constants.FIXED_PRICE_TYPE:
                price_type_name = str(rec.price_extra)
            else:
                price_type_name = "{} * {}".format(rec.price_extra, price_type)
                if rec.price_surcharge:
                    price_type_name = "{} + {}".format(
                        price_type_name, rec.price_surcharge
                    )
                if rec.price_round:
                    price_type_name = "{} {} {}".format(
                        price_type_name, _("rounded to"), rec.price_round
                    )
            rec.price_type_name = price_type_name

    def _compute_global_id(self):
        for rec in self:
            rec.global_id = self.get_global_id(rec)

    # -- Match Product
    def check_dimensions_match(self, dimensions):
        """
        Check if product matches any of rules
        :param dict dimensions: Product dimension attribute to check
        :return:True if matches else False
        """
        dimensions = constants.check_dim_vals(dimensions)
        for rule in self:
            rule_matched = True
            for line in rule.line_ids:
                if not constants.match_value(
                    dimensions[line.dimension], line.value_from, line.value_to
                ):
                    rule_matched = False
            if rule_matched:
                return True
        return False


#######################
# Dimension Rule Line #
#######################
class DimensionRuleLine(models.Model):
    _name = "ooops.dimension.rule.line"
    _description = "Dimension Rule Line"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    rule_id = fields.Many2one(
        string="Dimension Rule",
        comodel_name="ooops.dimension.rule",
        auto_join=True,
        ondelete="cascade",
    )
    dimension = fields.Selection(
        string="Dimension",
        selection=constants.DIMENSION_SELECTION,
        copy=True,
        required=True,
    )
    value_from = fields.Float(string="From", digits=(10, 4))
    value_to = fields.Float(string="To", digits=(10, 4))

    # -- Constraints
    @api.constrains("value_to", "value_from")
    def check_constraints(self):
        for rec in self:
            if rec.value_from == rec.value_to:
                raise ValidationError(
                    _("Same values in 'From' and 'To' fields are not allowed!")
                )

    # -- Compose name
    @api.depends("dimension", "value_to", "value_from")
    def _compute_name(self):
        for rec in self:
            if rec.dimension:
                value_from = rec.value_from
                value_to = rec.value_to
                if value_to and value_from and value_to == value_from:
                    rec.name = " ".join((rec.dimension, "=", str(value_from)))
                elif value_to > 0 and value_from > 0:
                    rec.name = " ".join(
                        (
                            rec.dimension,
                            _("between"),
                            str(value_from),
                            _("and"),
                            str(value_to),
                        )
                    )
                elif value_from > 0:
                    rec.name = " ".join((rec.dimension, ">", str(value_from)))
                elif value_to > 0:
                    rec.name = " ".join((rec.dimension, "<", str(value_to)))
                else:
                    rec.name = _("Invalid Expression")
