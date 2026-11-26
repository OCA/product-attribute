# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.fields import Command


class ProductAttributeValueMergeFinder(models.TransientModel):
    _name = "product.attribute.value.merge.finder"
    _description = "Find Duplicated Attribute Values"

    attribute_id = fields.Many2one(
        comodel_name="product.attribute", required=True, ondelete="cascade"
    )
    loose = fields.Boolean(
        string="Ignore Accents and Punctuation",
        help="Also group names that only differ in accents or punctuation, such as "
        '"2/3kg" and "2-3 kg".',
    )
    include_archived = fields.Boolean(string="Include Archived Values")
    lang_ids = fields.Many2many(
        comodel_name="res.lang",
        relation="product_attribute_value_merge_finder_lang_rel",
        column1="finder_id",
        column2="lang_id",
        string="Compare Names In",
        default=lambda self: self._default_lang_ids(),
        help="Two values are proposed as duplicates when they show the same name in "
        "any of these languages. By default, the languages of the internal users: "
        "translations nobody reviews can give two different values the same name.",
    )
    group_ids = fields.One2many(
        comodel_name="product.attribute.value.merge.finder.group",
        inverse_name="finder_id",
    )

    def _default_lang_ids(self):
        codes = self.env["product.attribute.value"]._merge_default_languages()
        return (
            self.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "in", codes)])
        )

    def action_search(self):
        self.ensure_one()
        values = (
            self.env["product.attribute.value"]
            .with_context(active_test=not self.include_archived)
            .search(
                [
                    ("attribute_id", "=", self.attribute_id.id),
                    ("merged_into_id", "=", False),
                ]
            )
        )
        groups = values._merge_find_duplicate_groups(
            loose=self.loose, langs=self.lang_ids.mapped("code")
        )
        stats = values._merge_statistics()
        self.group_ids = [Command.clear()] + [
            Command.create(
                {
                    "value_ids": [Command.set(group.ids)],
                    "names": " | ".join(group.mapped("name")),
                    "matches": " | ".join(matches),
                    "template_count": sum(
                        stats[value.id]["templates"] for value in group
                    ),
                }
            )
            for group, matches in groups
        ]
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Duplicated Values of %s", self.attribute_id.name),
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }


class ProductAttributeValueMergeFinderGroup(models.TransientModel):
    _name = "product.attribute.value.merge.finder.group"
    _description = "Duplicated Attribute Values"

    finder_id = fields.Many2one(
        comodel_name="product.attribute.value.merge.finder",
        required=True,
        ondelete="cascade",
    )
    value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_merge_finder_value_rel",
        column1="group_id",
        column2="value_id",
        string="Values",
        context={"active_test": False},
    )
    names = fields.Char()
    matches = fields.Char(string="Same Name In")
    template_count = fields.Integer(string="Products")

    def action_merge(self):
        self.ensure_one()
        return self.value_ids.action_merge()
