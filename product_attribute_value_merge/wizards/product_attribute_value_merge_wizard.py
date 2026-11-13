# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from markupsafe import Markup, escape

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import SQL


class ProductAttributeValueMergeWizard(models.TransientModel):
    _name = "product.attribute.value.merge.wizard"
    _description = "Merge Attribute Values"

    value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_merge_wizard_value_rel",
        column1="wizard_id",
        column2="value_id",
        string="Values",
        context={"active_test": False},
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute", compute="_compute_attribute_id"
    )
    keeper_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Value to Keep",
        help="The other values are merged into this one. Change it here: the list "
        "of values and the names follow.",
        compute="_compute_keeper_id",
        store=True,
        readonly=False,
        domain="[('id', 'in', value_ids), ('active', '=', True)]",
    )
    line_ids = fields.One2many(
        comodel_name="product.attribute.value.merge.wizard.line",
        inverse_name="wizard_id",
        compute="_compute_line_ids",
        store=True,
    )
    name_ids = fields.One2many(
        comodel_name="product.attribute.value.merge.wizard.name",
        inverse_name="wizard_id",
        compute="_compute_name_ids",
        store=True,
        readonly=False,
    )
    shared_product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        compute="_compute_shared_product_tmpl_ids",
        string="Products Using Both",
    )
    warning = fields.Html(compute="_compute_warning", sanitize=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        context = self.env.context
        if (
            "value_ids" in fields_list
            and not res.get("value_ids")
            and context.get("active_model") == "product.attribute.value"
            and context.get("active_ids")
        ):
            res["value_ids"] = [Command.set(context["active_ids"])]
        return res

    @api.depends("value_ids")
    def _compute_attribute_id(self):
        for wizard in self:
            wizard.attribute_id = wizard.value_ids.attribute_id[:1]

    @api.depends("value_ids")
    def _compute_keeper_id(self):
        for wizard in self:
            values = wizard.value_ids._origin
            if wizard.keeper_id._origin in values:
                continue
            wizard.keeper_id = values._merge_suggest_keeper()

    @api.depends("value_ids")
    def _compute_line_ids(self):
        for wizard in self:
            values = wizard.value_ids._origin
            stats = values._merge_statistics()
            xmlids = values.get_external_id()
            wizard.line_ids = [Command.clear()] + [
                Command.create(
                    {
                        "value_id": value.id,
                        "template_count": stats[value.id]["templates"],
                        "variant_count": stats[value.id]["variants"],
                        "record_count": stats[value.id]["records"],
                        "external_id": xmlids.get(value.id) or False,
                    }
                )
                for value in values
            ]

    @api.depends("value_ids", "keeper_id")
    def _compute_name_ids(self):
        normalize = self.env["product.attribute.value"]._merge_normalize
        for wizard in self:
            keeper = wizard.keeper_id._origin
            values = wizard.value_ids._origin
            if not keeper:
                wizard.name_ids = [Command.clear()]
                continue
            others = values - keeper
            raw = (keeper | others)._merge_raw_names()
            displayed = (keeper | others)._merge_displayed_names()
            lines = [Command.clear()]
            for code, lang_name in keeper._merge_languages():
                name = raw[keeper.id].get(code)
                fallback = False
                if not name:
                    # The kept value falls back to en_US here: take a real
                    # translation of a merged value, if any
                    name = next(
                        (raw[v.id][code] for v in others if raw[v.id].get(code)),
                        None,
                    )
                    if not name:
                        name = displayed[keeper.id][code]
                        fallback = True
                alternatives = []
                for value in keeper | others:
                    shown = displayed[value.id][code]
                    if shown != name and shown not in alternatives:
                        alternatives.append(shown)
                lines.append(
                    Command.create(
                        {
                            "lang": code,
                            "lang_name": lang_name,
                            "name": name,
                            "proposed_name": name,
                            "fallback": fallback,
                            "alternatives": " / ".join(alternatives),
                            "conflict": any(
                                normalize(alt) != normalize(name)
                                for alt in alternatives
                            ),
                        }
                    )
                )
            wizard.name_ids = lines

    @api.depends("value_ids", "keeper_id")
    def _compute_shared_product_tmpl_ids(self):
        for wizard in self:
            keeper = wizard.keeper_id._origin
            others = wizard.value_ids._origin - keeper
            if not keeper or not others:
                wizard.shared_product_tmpl_ids = False
                continue
            self.env.flush_all()
            self.env.cr.execute(
                SQL(
                    """SELECT DISTINCT a.product_tmpl_id
                       FROM product_template_attribute_value a
                       JOIN product_template_attribute_value b
                           ON b.attribute_line_id = a.attribute_line_id
                       WHERE a.product_attribute_value_id = %s
                           AND b.product_attribute_value_id IN %s
                           AND b.ptav_active""",
                    keeper.id,
                    tuple(others.ids),
                )
            )
            wizard.shared_product_tmpl_ids = [
                Command.set([row[0] for row in self.env.cr.fetchall()])
            ]

    @api.depends("value_ids", "keeper_id", "shared_product_tmpl_ids")
    def _compute_warning(self):
        for wizard in self:
            keeper = wizard.keeper_id._origin
            values = wizard.value_ids._origin
            others = values - keeper
            messages = []
            if len(values.attribute_id) > 1:
                messages.append(
                    self.env._("Only values of the same attribute can be merged.")
                )
            if wizard.shared_product_tmpl_ids:
                messages.append(
                    self.env._(
                        "Some products have the kept value and a merged one on the "
                        "same attribute line. There the merged value is not merged, "
                        "it stays active: rename it afterwards so both can be told "
                        "apart, or remove one of them from those products."
                    )
                )
            xmlids = others.get_external_id()
            for value in others.filtered(lambda v, xmlids=xmlids: xmlids.get(v.id)):
                messages.append(
                    self.env._(
                        "%(value)s has the external id %(xmlid)s: code or data "
                        "using it will reach the archived value.",
                        value=value.display_name,
                        xmlid=xmlids[value.id],
                    )
                )
            if keeper and others.filtered(
                lambda v, keeper=keeper: v.is_custom != keeper.is_custom
            ):
                messages.append(
                    self.env._(
                        "The values do not agree on free text; the kept value "
                        "decides it for every product."
                    )
                )
            for field, count in others._merge_unsupported_fields():
                messages.append(
                    self.env._(
                        "%(count)s %(model)s hold the merged values in %(field)s, "
                        "which is company dependent: they are not moved.",
                        count=count,
                        field=field.string,
                        model=self.env[field.model_name]._description,
                    )
                )
            for table, column, count in others._merge_unknown_references():
                messages.append(
                    self.env._(
                        "%(count)s rows of the table %(table)s (column %(column)s) "
                        "point to the merged values but belong to no installed "
                        "module: they are not moved.",
                        count=count,
                        table=table,
                        column=column,
                    )
                )
            wizard.warning = (
                Markup("<ul>%s</ul>")
                % Markup().join(Markup("<li>%s</li>") % escape(m) for m in messages)
                if messages
                else False
            )

    def action_merge(self):
        self.ensure_one()
        if not self.keeper_id:
            raise UserError(self.env._("Choose the value to keep."))
        # A language left on its en_US fallback keeps following en_US
        names = {
            line.lang: line.name
            for line in self.name_ids
            if not (line.fallback and line.name == line.proposed_name)
        }
        merge = self.env["product.attribute.value.merge"]._merge(
            self.keeper_id, self.value_ids, names
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.attribute.value.merge",
            "res_id": merge.id,
            "view_mode": "form",
            "target": "current",
        }


class ProductAttributeValueMergeWizardLine(models.TransientModel):
    _name = "product.attribute.value.merge.wizard.line"
    _description = "Merge Attribute Values: Candidate"

    wizard_id = fields.Many2one(
        comodel_name="product.attribute.value.merge.wizard",
        required=True,
        ondelete="cascade",
    )
    value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        required=True,
        ondelete="cascade",
        context={"active_test": False},
    )
    value_active = fields.Boolean(related="value_id.active", string="Active")
    is_keeper = fields.Boolean(compute="_compute_is_keeper", string="Kept")
    role = fields.Selection(
        selection=[("keep", "To Keep"), ("merge", "To Merge")],
        compute="_compute_is_keeper",
    )
    template_count = fields.Integer(string="Products")
    variant_count = fields.Integer(string="Variants")
    record_count = fields.Integer(string="Other Records")
    external_id = fields.Char()

    @api.depends("wizard_id.keeper_id", "value_id")
    def _compute_is_keeper(self):
        for line in self:
            line.is_keeper = line.value_id == line.wizard_id.keeper_id
            line.role = "keep" if line.is_keeper else "merge"


class ProductAttributeValueMergeWizardName(models.TransientModel):
    _name = "product.attribute.value.merge.wizard.name"
    _description = "Merge Attribute Values: Name"

    wizard_id = fields.Many2one(
        comodel_name="product.attribute.value.merge.wizard",
        required=True,
        ondelete="cascade",
    )
    lang = fields.Char(required=True)
    lang_name = fields.Char(string="Language")
    name = fields.Char(string="Kept Name", required=True)
    alternatives = fields.Char(string="Other Names")
    conflict = fields.Boolean()
    proposed_name = fields.Char()
    fallback = fields.Boolean(help="The kept value shows the en_US name here.")
