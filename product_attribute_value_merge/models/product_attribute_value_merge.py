# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2.errors import LockNotAvailable
from psycopg2.extras import Json

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import SQL

PTAV = "product.template.attribute.value"
PTAL = "product.template.attribute.line"


class ProductAttributeValueMerge(models.Model):
    """A merge of attribute values into one, with what it moved so it can be
    undone. Product attribute values are moved in place (SQL), keeping their id:
    variants and their combinations, and therefore stock, sales and accounting,
    do not change."""

    _name = "product.attribute.value.merge"
    _description = "Attribute Value Merge"
    _order = "id desc"

    keeper_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Kept Value",
        required=True,
        readonly=True,
        ondelete="cascade",
        context={"active_test": False},
    )
    attribute_id = fields.Many2one(related="keeper_id.attribute_id", store=True)
    value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_merge_value_rel",
        column1="merge_id",
        column2="value_id",
        string="Merged Values",
        readonly=True,
        context={"active_test": False},
    )
    kept_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_merge_kept_value_rel",
        column1="merge_id",
        column2="value_id",
        string="Values Left on Some Products",
        readonly=True,
        context={"active_test": False},
        help="Merged values that stay active because a product has them next to "
        "the kept value on the same attribute line.",
    )
    archived_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_merge_archived_value_rel",
        column1="merge_id",
        column2="value_id",
        string="Values Archived by the Merge",
        readonly=True,
        context={"active_test": False},
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Merged By",
        default=lambda self: self.env.user,
        readonly=True,
    )
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    state = fields.Selection(
        selection=[("done", "Merged"), ("undone", "Undone")],
        default="done",
        readonly=True,
    )
    change_ids = fields.One2many(
        comodel_name="product.attribute.value.merge.change",
        inverse_name="merge_id",
        readonly=True,
    )
    name_before = fields.Json(readonly=True)
    name_after = fields.Json(readonly=True)
    values_before = fields.Json(readonly=True)
    values_after = fields.Json(readonly=True)
    undo_user_id = fields.Many2one(
        comodel_name="res.users", string="Undone By", readonly=True
    )
    undo_date = fields.Datetime(readonly=True)
    undo_report = fields.Text(readonly=True)

    @api.depends("keeper_id.name", "value_ids.name")
    def _compute_display_name(self):
        for merge in self:
            merge.display_name = "{} ← {}".format(
                merge.keeper_id.name, ", ".join(merge.value_ids.mapped("name"))
            )

    # === SQL MOVES === #

    @api.model
    def _lock_values(self, values):
        try:
            with self.env.cr.savepoint(flush=False):
                self.env.cr.execute(
                    SQL(
                        "SELECT id FROM product_attribute_value WHERE id IN %s"
                        " FOR UPDATE NOWAIT",
                        tuple(values.ids),
                    )
                )
        except LockNotAvailable:
            raise UserError(
                self.env._(
                    "Someone else is changing these values right now. "
                    "Try again in a moment."
                )
            ) from None

    @api.model
    def _invalidate_moved(self, records, field):
        records.invalidate_recordset([field.name], flush=False)
        for inverse in self.env.registry.field_inverses[field]:
            self.env[inverse.model_name].invalidate_model([inverse.name], flush=False)

    @api.model
    def _move_many2one(self, model_name, field_name, ids, from_id, to_id):
        """Point ``field_name`` of the records ``ids`` still holding ``from_id`` to
        ``to_id``, keeping the ORM informed. Return the ids changed."""
        model = self.env[model_name].with_context(active_test=False)
        field = model._fields[field_name]
        if not ids:
            return []
        records = model.browse(ids)
        records.modified([field_name], before=True)
        self.env.cr.execute(
            SQL(
                "UPDATE %s SET %s = %s WHERE id IN %s AND %s = %s RETURNING id",
                SQL.identifier(model._table),
                SQL.identifier(field.name),
                to_id,
                tuple(ids),
                SQL.identifier(field.name),
                from_id,
            )
        )
        changed = [row[0] for row in self.env.cr.fetchall()]
        self._invalidate_moved(records, field)
        records.modified([field_name])
        return changed

    @api.model
    def _select_many2one(self, model_name, field_name, value_id, extra=None):
        model = self.env[model_name]
        self.env.cr.execute(
            SQL(
                "SELECT id FROM %s WHERE %s = %s %s",
                SQL.identifier(model._table),
                SQL.identifier(model._fields[field_name].name),
                value_id,
                extra or SQL(),
            )
        )
        return [row[0] for row in self.env.cr.fetchall()]

    @api.model
    def _many2many_owners(self, field, value_id, owner_ids=None):
        query = SQL(
            "SELECT %s FROM %s WHERE %s = %s",
            SQL.identifier(field.column1),
            SQL.identifier(field.relation),
            SQL.identifier(field.column2),
            value_id,
        )
        if owner_ids is not None:
            if not owner_ids:
                return set()
            query = SQL(
                "%s AND %s IN %s",
                query,
                SQL.identifier(field.column1),
                tuple(owner_ids),
            )
        self.env.cr.execute(query)
        return {row[0] for row in self.env.cr.fetchall()}

    @api.model
    def _relink_many2many(self, model_name, field_name, owner_ids, add_id, remove_id):
        """On the records ``owner_ids`` link ``add_id`` where it is missing and
        unlink ``remove_id`` where it is linked. Return the owners ``add_id`` was
        added to."""
        model = self.env[model_name].with_context(active_test=False)
        field = model._fields[field_name]
        if not owner_ids:
            return set()
        records = model.browse(owner_ids)
        records.modified([field_name], before=True)
        added = set(owner_ids) - self._many2many_owners(field, add_id, owner_ids)
        if remove_id:
            self.env.cr.execute(
                SQL(
                    "DELETE FROM %s WHERE %s = %s AND %s IN %s",
                    SQL.identifier(field.relation),
                    SQL.identifier(field.column2),
                    remove_id,
                    SQL.identifier(field.column1),
                    tuple(owner_ids),
                )
            )
        if added:
            self.env.cr.execute(
                SQL(
                    "INSERT INTO %s (%s, %s) SELECT unnest(%s::int[]), %s",
                    SQL.identifier(field.relation),
                    SQL.identifier(field.column1),
                    SQL.identifier(field.column2),
                    sorted(added),
                    add_id,
                )
            )
        self._invalidate_moved(records, field)
        records.modified([field_name])
        return added

    @api.model
    def _unlink_many2many(self, model_name, field_name, owner_ids, value_id):
        model = self.env[model_name].with_context(active_test=False)
        field = model._fields[field_name]
        if not owner_ids:
            return
        records = model.browse(owner_ids)
        records.modified([field_name], before=True)
        self.env.cr.execute(
            SQL(
                "DELETE FROM %s WHERE %s = %s AND %s IN %s",
                SQL.identifier(field.relation),
                SQL.identifier(field.column2),
                value_id,
                SQL.identifier(field.column1),
                tuple(owner_ids),
            )
        )
        self._invalidate_moved(records, field)
        records.modified([field_name])

    @api.model
    def _shared_lines(self, keeper, value):
        """Attribute lines holding both values, as {line: product value of
        ``value`` is active}. The unique constraint per line forbids moving the
        product value there. An archived one is left as it is: nothing shows it
        any more. An active one keeps the merged value in use."""
        self.env.cr.execute(
            SQL(
                """SELECT a.attribute_line_id, bool_or(a.ptav_active)
                   FROM product_template_attribute_value a
                   JOIN product_template_attribute_value b
                       ON b.attribute_line_id = a.attribute_line_id
                   WHERE a.product_attribute_value_id = %s
                       AND b.product_attribute_value_id = %s
                   GROUP BY a.attribute_line_id""",
                value.id,
                keeper.id,
            )
        )
        return dict(self.env.cr.fetchall())

    @api.model
    def _set_raw_name(self, value, name):
        value.flush_recordset(["name"])
        value.modified(["name"], before=True)
        self.env.cr.execute(
            SQL(
                "UPDATE product_attribute_value SET name = %s WHERE id = %s",
                Json(name),
                value.id,
            )
        )
        value.invalidate_recordset(["name"], flush=False)
        value.modified(["name"])

    # === MERGE === #

    @api.model
    def _merge_check(self, keeper, values):
        if not keeper or not values:
            raise UserError(self.env._("Select at least two values to merge."))
        if len((keeper | values).attribute_id) > 1:
            raise UserError(
                self.env._("Only values of the same attribute can be merged.")
            )
        if not keeper.active:
            raise UserError(self.env._("The value to keep must be active."))
        self.check_access("read")
        if merged := values.filtered("merged_into_id"):
            raise UserError(
                self.env._(
                    "These values were already merged: %(values)s",
                    values=", ".join(merged.mapped("display_name")),
                )
            )
        keeper.check_access("write")

    @api.model
    def _merge_value(self, keeper, value, references):
        """Move to ``keeper`` what points to ``value``, except on the lines holding
        both. Return the changes to log and whether ``value`` stays in use on such
        a line."""
        shared = self._shared_lines(keeper, value)
        extra = (
            SQL("AND attribute_line_id NOT IN %s", tuple(shared)) if shared else None
        )
        ptav_ids = self._select_many2one(
            PTAV, "product_attribute_value_id", value.id, extra
        )
        moved = self._move_many2one(
            PTAV, "product_attribute_value_id", ptav_ids, value.id, keeper.id
        )
        changes = [("ptav", PTAV, "product_attribute_value_id", moved, [])]
        line_field = self.env[PTAL]._fields["value_ids"]
        lines = self._many2many_owners(line_field, value.id) - set(shared)
        added = self._relink_many2many(PTAL, "value_ids", lines, keeper.id, value.id)
        changes.append(("line", PTAL, "value_ids", lines, added))
        for model_name, field_name in references:
            field = self.env[model_name]._fields[field_name]
            if field.type == "many2one":
                ids = self._select_many2one(model_name, field_name, value.id)
                moved = self._move_many2one(
                    model_name, field_name, ids, value.id, keeper.id
                )
                changes.append(("many2one", model_name, field_name, moved, []))
            else:
                owners = self._many2many_owners(field, value.id)
                added = self._relink_many2many(
                    model_name, field_name, owners, keeper.id, value.id
                )
                changes.append(("many2many", model_name, field_name, owners, added))
        return [
            {
                "kind": kind,
                "model": model_name,
                "field_name": field_name,
                "value_id": value.id,
                "res_ids": sorted(ids),
                "added_ids": sorted(added),
            }
            for kind, model_name, field_name, ids, added in changes
            if ids
        ], any(shared.values())

    @api.model
    def _merge_name(self, name_before, names):
        """Stored translations of the kept value once it shows ``names``."""
        name_after = dict(name_before)
        if names.get("en_US"):
            name_after["en_US"] = names["en_US"]
        for code, name in names.items():
            # A language without its own name shows en_US: store it only when the
            # name asked for differs from what it would show
            if name and name != name_after.get(code, name_after.get("en_US")):
                name_after[code] = name
        return name_after

    @api.model
    def _merge_fill(self, keeper, values):
        """Fill the empty fields of the kept value from the merged ones. Return the
        values before and after."""
        values_before, values_after = {}, {}
        for group in keeper._merge_fill_field_groups():
            if any(keeper[name] for name in group):
                continue
            source = keeper._merge_fill_source(group, values)
            if source:
                for name in group:
                    values_before[name] = keeper[name]
                    values_after[name] = source[name]
        if values_after:
            keeper.write(values_after)
        return values_before, values_after

    @api.model
    def _merge(self, keeper, values, names=None):
        """Merge ``values`` into ``keeper``. ``names`` maps language codes to the
        name the kept value must show in them. Return the merge record."""
        values = values.with_context(active_test=False) - keeper
        self._merge_check(keeper, values)
        self.env.flush_all()
        self._lock_values(keeper | values)
        name_before = (keeper | values)._merge_raw_names()[keeper.id]
        # The log drives SQL on undo: only this code writes it
        merge = self.sudo().create(
            {
                "keeper_id": keeper.id,
                "value_ids": [Command.set(values.ids)],
                "user_id": self.env.user.id,
            }
        )
        references = self.env["product.attribute.value"]._merge_reference_fields()
        changes = []
        kept_values = values.browse()
        for value in values:
            value_changes, shared = self._merge_value(keeper, value, references)
            changes += value_changes
            if shared:
                kept_values |= value
        if kept_values == values and not changes:
            raise UserError(
                self.env._(
                    "Nothing to merge: every product using these values also has the "
                    "kept value on the same attribute line."
                )
            )
        merge.change_ids = [Command.create(change) for change in changes]
        self.env[PTAV].browse(
            [
                i
                for change in changes
                if change["kind"] == "ptav"
                for i in change["res_ids"]
            ]
        )._check_valid_values()
        name_after = self._merge_name(name_before, names or {})
        if name_after != name_before:
            self._set_raw_name(keeper, name_after)
        values_before, values_after = self._merge_fill(keeper, values)
        merged = values - kept_values
        archived = merged.filtered("active")
        merged.write({"active": False, "merged_into_id": keeper.id})
        merge.write(
            {
                "kept_value_ids": [Command.set(kept_values.ids)],
                "archived_value_ids": [Command.set(archived.ids)],
                "name_before": name_before,
                "name_after": name_after,
                "values_before": values_before,
                "values_after": values_after,
            }
        )
        self.env.flush_all()
        return merge.sudo(False)

    # === UNDO === #

    def action_undo(self):
        self.ensure_one()
        if self.state != "done":
            raise UserError(self.env._("This merge is already undone."))
        values = self.value_ids
        involved = self.keeper_id | values
        later = (
            self.with_context(active_test=False)
            .search(
                [
                    ("id", ">", self.id),
                    ("state", "=", "done"),
                    "|",
                    ("keeper_id", "in", involved.ids),
                    ("value_ids", "in", involved.ids),
                ]
            )
            .sorted("id")
        )
        if later:
            raise UserError(
                self.env._(
                    "These values were merged again later. Undo these merges first: "
                    "%(merges)s",
                    merges=", ".join(later.mapped("display_name")),
                )
            )
        self.keeper_id.check_access("write")
        self.env.flush_all()
        self._lock_values(involved)
        report = []
        changes = self.change_ids.sorted(lambda c: (c.kind != "ptav", c.id))
        restored_ptavs = []
        for change in changes:
            restored = change._undo(report)
            if change.kind == "ptav":
                restored_ptavs += restored
        self._undo_keeper(report)
        merged = values.filtered(lambda v: v.merged_into_id == self.keeper_id)
        merged.write({"merged_into_id": False})
        (merged & self.archived_value_ids).write({"active": True})
        # Lines hide archived values: check once the merged ones are active again
        self.env[PTAV].browse(restored_ptavs)._check_valid_values()
        self.env.flush_all()
        self.sudo().write(
            {
                "state": "undone",
                "undo_user_id": self.env.user.id,
                "undo_date": fields.Datetime.now(),
                "undo_report": "\n".join(report),
            }
        )
        return True

    def _undo_keeper(self, report):
        keeper = self.keeper_id
        current = keeper._merge_raw_names()[keeper.id]
        restored = dict(current)
        for code, after in (self.name_after or {}).items():
            before = (self.name_before or {}).get(code)
            if after == before:
                continue
            if current.get(code) != after:
                report.append(
                    self.env._(
                        "The name of %(value)s in %(lang)s was changed after the "
                        "merge and is left as it is.",
                        value=keeper.display_name,
                        lang=code,
                    )
                )
                continue
            if before is None:
                restored.pop(code)
            else:
                restored[code] = before
        if restored != current:
            self._set_raw_name(keeper, restored)
        vals = {}
        for name, after in (self.values_after or {}).items():
            if keeper[name] == after:
                vals[name] = self.values_before[name]
            else:
                report.append(
                    self.env._(
                        "%(field)s of %(value)s was changed after the merge and is "
                        "left as it is.",
                        field=keeper._fields[name].string,
                        value=keeper.display_name,
                    )
                )
        if vals:
            keeper.write(vals)


class ProductAttributeValueMergeChange(models.Model):
    """Records moved by a merge for one merged value and one field. Ids are plain
    integers: an undo checks the records still exist and still hold the kept
    value before touching them."""

    _name = "product.attribute.value.merge.change"
    _description = "Attribute Value Merge Change"
    _order = "id"

    merge_id = fields.Many2one(
        comodel_name="product.attribute.value.merge",
        required=True,
        ondelete="cascade",
        index=True,
    )
    kind = fields.Selection(
        selection=[
            ("ptav", "Product values"),
            ("line", "Product attribute lines"),
            ("many2one", "Records"),
            ("many2many", "Record lists"),
        ],
        required=True,
    )
    model = fields.Char(required=True)
    field_name = fields.Char(required=True)
    model_description = fields.Char(compute="_compute_descriptions")
    field_description = fields.Char(compute="_compute_descriptions")
    value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Merged Value",
        ondelete="set null",
        context={"active_test": False},
    )
    res_ids = fields.Json(string="Records")
    added_ids = fields.Json(
        string="Kept Value Added To",
        help="Records that did not hold the kept value before the merge.",
    )
    record_count = fields.Integer(compute="_compute_record_count")

    @api.depends("model", "field_name")
    def _compute_descriptions(self):
        for change in self:
            model = self.env.get(change.model)
            field = model._fields.get(change.field_name) if model is not None else None
            change.model_description = (
                model._description if model is not None else change.model
            )
            change.field_description = field.string if field else change.field_name

    @api.depends("res_ids")
    def _compute_record_count(self):
        for change in self:
            change.record_count = len(change.res_ids or [])

    def _is_supported(self):
        """Whether the logged field is one a merge moves, of the kind logged: an
        uninstalled module may have removed it."""
        if (self.model, self.field_name) == (PTAV, "product_attribute_value_id"):
            return self.kind == "ptav"
        if (self.model, self.field_name) == (PTAL, "value_ids"):
            return self.kind == "line"
        references = self.env["product.attribute.value"]._merge_reference_fields()
        if (self.model, self.field_name) not in references:
            return False
        field = self.env[self.model]._fields[self.field_name]
        return self.kind == field.type

    def _existing_ids(self, ids):
        if not ids:
            return []
        model = self.env[self.model]
        self.env.cr.execute(
            SQL(
                "SELECT id FROM %s WHERE id IN %s",
                SQL.identifier(model._table),
                tuple(ids),
            )
        )
        return [row[0] for row in self.env.cr.fetchall()]

    def _undo(self, report):
        self.ensure_one()
        merge = self.merge_id
        keeper, value = merge.keeper_id, self.value_id
        if not value:
            report.append(
                self.env._(
                    "A merged value was deleted; %(count)s %(model)s keep %(keeper)s.",
                    count=self.record_count,
                    model=self.model_description,
                    keeper=keeper.display_name,
                )
            )
            return []
        if not self._is_supported():
            report.append(
                self.env._(
                    "%(model)s (%(field)s) can no longer be restored: %(count)s "
                    "records keep %(keeper)s.",
                    model=self.model_description,
                    field=self.field_description,
                    count=self.record_count,
                    keeper=keeper.display_name,
                )
            )
            return []
        if self.kind == "line":
            restored = self._undo_lines(keeper, value)
        elif self.kind == "many2many":
            restored = self._undo_many2many(keeper, value)
        else:
            ids = self.res_ids
            if self.kind == "ptav":
                ids = self._ptavs_free_for(value, ids)
            restored = merge._move_many2one(
                self.model, self.field_name, ids, keeper.id, value.id
            )
        skipped = len(self.res_ids) - len(restored)
        if skipped:
            report.append(
                self.env._(
                    "%(count)s of %(total)s %(model)s (%(field)s) were changed after "
                    "the merge and keep their current value.",
                    count=skipped,
                    total=len(self.res_ids),
                    model=self.model_description,
                    field=self.field_description,
                )
            )
        return restored

    def _ptavs_free_for(self, value, ids):
        """Product values whose line has no other product value for ``value``:
        undoing the rest would break the unique constraint per line."""
        if not ids:
            return []
        self.env.cr.execute(
            SQL(
                """SELECT a.id FROM product_template_attribute_value a
                   WHERE a.id IN %s AND NOT EXISTS (
                       SELECT 1 FROM product_template_attribute_value b
                       WHERE b.attribute_line_id = a.attribute_line_id
                           AND b.product_attribute_value_id = %s)""",
                tuple(ids),
                value.id,
            )
        )
        return [row[0] for row in self.env.cr.fetchall()]

    def _undo_lines(self, keeper, value):
        """Give each line back the merged value where its product value is active
        again, and remove the kept value where the merge added it and no active
        product value uses it any more. A line whose product value was removed
        after the merge stays as it is."""
        lines = self._existing_ids(self.res_ids)
        if not lines:
            return []
        self.env.cr.execute(
            SQL(
                """SELECT attribute_line_id, product_attribute_value_id
                   FROM product_template_attribute_value
                   WHERE attribute_line_id IN %s
                       AND product_attribute_value_id IN %s AND ptav_active""",
                tuple(lines),
                (keeper.id, value.id),
            )
        )
        active = set(self.env.cr.fetchall())
        restored = [line for line in lines if (line, value.id) in active]
        merge = self.merge_id
        merge._relink_many2many(self.model, self.field_name, restored, value.id, None)
        unused = [
            line
            for line in set(self.added_ids or []) & set(lines)
            if (line, keeper.id) not in active
        ]
        merge._unlink_many2many(self.model, self.field_name, unused, keeper.id)
        return restored

    def _undo_many2many(self, keeper, value):
        """Give the merged value back to the records that still hold the kept
        value, and remove the kept value from those the merge added it to."""
        field = self.env[self.model]._fields[self.field_name]
        merge = self.merge_id
        owners = merge._many2many_owners(field, keeper.id, self.res_ids)
        merge._relink_many2many(
            self.model, self.field_name, sorted(owners), value.id, None
        )
        merge._unlink_many2many(
            self.model,
            self.field_name,
            sorted(owners & set(self.added_ids or [])),
            keeper.id,
        )
        return owners
