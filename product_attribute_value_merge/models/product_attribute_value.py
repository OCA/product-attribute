# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re
import unicodedata
from collections import defaultdict

from odoo import api, fields, models
from odoo.tools import SQL

# Moved apart by the merge: the unique constraint of the product attribute values
# per line decides which lines can be merged
MERGE_SPECIAL_FIELDS = {
    ("product.template.attribute.value", "product_attribute_value_id"),
    ("product.template.attribute.line", "value_ids"),
    ("product.attribute.value", "merged_into_id"),
}


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    merged_into_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Merged Into",
        readonly=True,
        copy=False,
        index="btree_not_null",
        ondelete="set null",
    )

    @api.model
    def _merge_normalize(self, name, loose=False):
        """Key under which two names count as the same one: case and spaces are
        ignored, and in loose mode accents and punctuation too ("2/3kg" and
        "2-3 kg")."""
        name = re.sub(r"\s+", "", name or "").casefold()
        if loose:
            name = "".join(
                char
                for char in unicodedata.normalize("NFKD", name)
                if not unicodedata.combining(char)
            )
            name = re.sub(r"[\W_]+", "-", name).strip("-")
        return name

    @api.model
    def _merge_languages(self):
        """Installed languages plus en_US, which holds the source name even when
        it is not installed."""
        languages = self.env["res.lang"].get_installed()
        if "en_US" not in dict(languages):
            languages = [("en_US", "English (US)")] + languages
        return languages

    def _merge_raw_names(self):
        """Stored translations of each value, without the fallback to en_US."""
        if not self:
            return {}
        self.flush_recordset(["name"])
        self.env.cr.execute(
            SQL(
                "SELECT id, name FROM product_attribute_value WHERE id IN %s",
                tuple(self.ids),
            )
        )
        return dict(self.env.cr.fetchall())

    def _merge_displayed_names(self):
        """Name each language shows for each value, fallback included."""
        names = defaultdict(dict)
        for code, _lang_name in self._merge_languages():
            for value in self.with_context(lang=code):
                names[value.id][code] = value.name
        return names

    @api.model
    def _merge_default_languages(self):
        """Languages compared by default to find duplicates: those of the internal
        users. Translations nobody reviews (customer languages) can give two
        different values the same name."""
        langs = set(
            self.env["res.users"].sudo().search([("share", "=", False)]).mapped("lang")
        )
        installed = dict(self._merge_languages())
        return [code for code in installed if code in langs] or list(installed)

    def _merge_find_duplicate_groups(self, loose=False, langs=None):
        """Groups of values of the same attribute that show the same name in any of
        the languages ``langs`` (all by default), as (values, matches) where
        matches are the "language: name" pairs that joined them. Values created
        from the user interface often hold only the creator's language, so a single
        language would miss them."""
        names = self._merge_displayed_names()
        parent = {value.id: value.id for value in self}

        def find(value_id):
            while parent[value_id] != value_id:
                value_id = parent[value_id]
            return value_id

        first = {}
        matches = []
        for value in self:
            for code, name in names[value.id].items():
                if langs is not None and code not in langs:
                    continue
                key = (value.attribute_id.id, code, self._merge_normalize(name, loose))
                if key in first:
                    parent[find(value.id)] = find(first[key])
                    matches.append((value.id, f"{code}: {name}"))
                else:
                    first[key] = value.id
        groups = defaultdict(list)
        for value in self:
            groups[find(value.id)].append(value.id)
        group_matches = defaultdict(list)
        for value_id, match in matches:
            if match not in group_matches[find(value_id)]:
                group_matches[find(value_id)].append(match)
        return [
            (self.browse(ids), group_matches[root])
            for root, ids in groups.items()
            if len(ids) > 1
        ]

    @api.model
    def _merge_reference_fields(self):
        """Stored many2one and many2many fields pointing to attribute values that a
        merge moves to the kept value, as (model name, field name). Related fields
        follow their source and company dependent ones are not supported."""
        result = []
        relations = set()
        for model_name in self.env.registry:
            model = self.env[model_name]
            if (
                model._transient
                or model._abstract
                or not model._auto
                or model_name.startswith("product.attribute.value.merge")
            ):
                continue
            for field in model._fields.values():
                if (
                    field.type not in ("many2one", "many2many")
                    or field.comodel_name != self._name
                    or not field.store
                    or field.related
                    or field.inherited
                    or field.company_dependent
                    or (model_name, field.name) in MERGE_SPECIAL_FIELDS
                ):
                    continue
                if field.type == "many2many":
                    if field.relation in relations:
                        continue
                    relations.add(field.relation)
                result.append((model_name, field.name))
        return result

    def _merge_unknown_references(self):
        """Columns with a foreign key to attribute values that no field of the
        registry covers (a table of an uninstalled module, a leftover of a
        migration), with how many of their rows point to these values, as
        (table, column, count). The merge does not move them."""
        known = set()
        for model_name in self.env.registry:
            model = self.env[model_name]
            if model._abstract or not model._auto:
                continue
            for field in model._fields.values():
                if not field.store or field.type not in ("many2one", "many2many"):
                    continue
                if field.type == "many2one" and field.comodel_name == self._name:
                    known.add((model._table, field.name))
                elif field.type == "many2many":
                    if field.comodel_name == self._name:
                        known.add((field.relation, field.column2))
                    if model_name == self._name:
                        known.add((field.relation, field.column1))
        self.env.cr.execute(
            SQL(
                """SELECT cl.relname, att.attname
                   FROM pg_constraint con
                   JOIN pg_class cl ON cl.oid = con.conrelid
                   JOIN pg_attribute att
                       ON att.attrelid = con.conrelid AND att.attnum = con.conkey[1]
                   WHERE con.contype = 'f' AND con.confrelid = %s::regclass""",
                self._table,
            )
        )
        result = []
        for table, column in self.env.cr.fetchall():
            if (table, column) in known or not self:
                continue
            self.env.cr.execute(
                SQL(
                    "SELECT count(*) FROM %s WHERE %s IN %s",
                    SQL.identifier(table),
                    SQL.identifier(column),
                    tuple(self.ids),
                )
            )
            count = self.env.cr.fetchone()[0]
            if count:
                result.append((table, column, count))
        return result

    def _merge_unsupported_fields(self):
        """Company dependent fields holding these values, which a merge cannot
        move, with how many records hold them, as (field, count)."""
        result = []
        if not self:
            return result
        self.env.flush_all()
        ids = tuple(str(value_id) for value_id in self.ids)
        for model_name in self.env.registry:
            model = self.env[model_name]
            if model._transient or model._abstract or not model._auto:
                continue
            for field in model._fields.values():
                if field.comodel_name != self._name or not field.company_dependent:
                    continue
                self.env.cr.execute(
                    SQL(
                        """SELECT count(*) FROM %s WHERE EXISTS (
                               SELECT 1 FROM jsonb_each_text(%s) WHERE value IN %s)""",
                        SQL.identifier(model._table),
                        SQL.identifier(field.name),
                        ids,
                    )
                )
                count = self.env.cr.fetchone()[0]
                if count:
                    result.append((field, count))
        return result

    def _merge_statistics(self):
        """Usage of each value: product templates, variants and other records."""
        stats = {
            value.id: {"templates": 0, "variants": 0, "records": 0} for value in self
        }
        if not self:
            return stats
        self.env.flush_all()
        ids = tuple(self.ids)
        cr = self.env.cr
        cr.execute(
            SQL(
                """SELECT ptav.product_attribute_value_id,
                          count(DISTINCT ptav.product_tmpl_id),
                          count(DISTINCT pvc.product_product_id)
                   FROM product_template_attribute_value ptav
                   LEFT JOIN product_variant_combination pvc
                       ON pvc.product_template_attribute_value_id = ptav.id
                   WHERE ptav.product_attribute_value_id IN %s
                   GROUP BY ptav.product_attribute_value_id""",
                ids,
            )
        )
        for value_id, templates, variants in cr.fetchall():
            stats[value_id].update(templates=templates, variants=variants)
        for model_name, field_name in self._merge_reference_fields():
            model = self.env[model_name]
            field = model._fields[field_name]
            if field.type == "many2one":
                table, column = model._table, field.name
            else:
                table, column = field.relation, field.column2
            cr.execute(
                SQL(
                    "SELECT %s, count(*) FROM %s WHERE %s IN %s GROUP BY %s",
                    SQL.identifier(column),
                    SQL.identifier(table),
                    SQL.identifier(column),
                    ids,
                    SQL.identifier(column),
                )
            )
            for value_id, count in cr.fetchall():
                stats[value_id]["records"] += count
        return stats

    def _merge_keeper_sort_key(self, stats, xmlids):
        """Sort key of a merge candidate, the lowest is suggested as the value to
        keep: active, referenced by code or data, then the most used."""
        self.ensure_one()
        return (
            not self.active,
            not xmlids.get(self.id),
            -stats[self.id]["templates"],
            -stats[self.id]["records"],
            self.id,
        )

    def _merge_suggest_keeper(self):
        stats = self._merge_statistics()
        xmlids = self.get_external_id()
        return self.sorted(lambda value: value._merge_keeper_sort_key(stats, xmlids))[
            :1
        ]

    @api.model
    def _merge_fill_field_groups(self):
        """Fields of the kept value filled from a merged one when all the fields of
        the group are empty on the kept value."""
        return [("html_color",)]

    def _merge_fill_source(self, group, values):
        """Merged value among ``values`` whose fields of ``group`` fill the kept
        value (self), if any."""
        self.ensure_one()
        return values.filtered(lambda v: any(v[name] for name in group))[:1]

    def action_merge(self):
        """Open the merge wizard with these values. From a single value, its
        duplicates are proposed with it."""
        values = self
        if len(self) == 1:
            candidates = self.search([("attribute_id", "=", self.attribute_id.id)])
            langs = self._merge_default_languages()
            for group, _matches in candidates._merge_find_duplicate_groups(langs=langs):
                if self in group:
                    values = group
                    break
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Merge Attribute Values"),
            "res_model": "product.attribute.value.merge.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_value_ids": values.ids},
        }
