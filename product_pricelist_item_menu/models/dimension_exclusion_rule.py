from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..constants import constants


#######################################
# Dimension Exclusion Rule
#######################################
class DimensionExclusionRule(models.Model):
    _name = "ooops.dimension.exclusion.rule"
    _description = "Dimension Exclusion Rule"
    # Used to compose rules in case
    # they cannot be created explicitly

    name = fields.Text(string="Name", compute="_compute_name", store=True)
    rule_name = fields.Char(
        string="Rule name",
        help="User assigned name",
    )
    line_ids = fields.One2many(
        string="For dimensions",
        required=True,
        auto_join=True,
        comodel_name="ooops.dimension.exclusion.rule.line",
        inverse_name="rule_id",
    )
    product_tmpl_ids = fields.Many2many(
        string="Products",
        comodel_name="product.template",
    )
    value_ids = fields.Many2many(
        string="Attribute Values to exclude",
        comodel_name="product.attribute.value",
        relation="ooops_der_exclusion_pav_rel",
        column1="exclusion_rule_id",
        column2="pav_id",
    )

    @api.depends("line_ids.name")
    def _compute_name(self):
        """Compose name"""
        for rec in self:
            if len(rec.line_ids) == 1:
                rec.name = rec.line_ids[0].name
            else:
                rec.name = "\nAND ".join([line.name for line in rec.line_ids])

    def update_exclusion_rules_for_product_template(
        self, new_der_ids, product_template_id
    ):
        """
        Updating dimension exclusion rules for product template
        param : new_der_ids : list of ids 'ooops.dimension.exclusion.rule' model
        param : product_template_id : singleton recordset of model 'product.template'
        return : None
        """
        new_dimension_exclusion_rule_ids = self.browse(new_der_ids)
        current_dimension_exclusion_rule_ids = product_template_id.der_ids
        for record in current_dimension_exclusion_rule_ids:
            record.update(
                {
                    "product_tmpl_ids": [(3, 0, product_template_id.id)],
                }
            )
        for record in new_dimension_exclusion_rule_ids:
            record.update(
                {
                    "product_tmpl_ids": [(4, product_template_id.id)],
                }
            )


##############################################
# Dimension Exclusion Rule Line
##############################################
class DimensionExclusionRuleLine(models.Model):
    _name = "ooops.dimension.exclusion.rule.line"
    _description = "Dimension Exclusion Rule Line"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    rule_id = fields.Many2one(
        string="Dimension Rule",
        comodel_name="ooops.dimension.exclusion.rule",
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
