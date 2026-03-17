# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

MAX_ATTRIBUTE_GROUPBY = 3


class ProductProduct(models.Model):
    _inherit = "product.product"

    attribute_group_by_1 = fields.Char(
        string="Attribute Group By 1",
        store=False,
        help="Technical field for attribute groupBy slot 1",
    )
    attribute_group_by_2 = fields.Char(
        string="Attribute Group By 2",
        store=False,
        help="Technical field for attribute groupBy slot 2",
    )
    attribute_group_by_3 = fields.Char(
        string="Attribute Group By 3",
        store=False,
        help="Technical field for attribute groupBy slot 3",
    )

    @api.model
    def get_groupby_attribute_fields(self):
        attributes = self.env["product.attribute"].search(
            [("exclude_from_groupby", "=", False)],
            order="name",
        )
        return [{"id": attr.id, "label": attr.name} for attr in attributes]

    @api.model
    def _resolve_attribute_id(self, slot, domain):
        context_key = "groupby_attribute_id_%d" % slot
        attribute_id = self.env.context.get(context_key)
        if attribute_id:
            return attribute_id

        all_requested = [
            self.env.context.get("groupby_attribute_id_%d" % s)
            for s in range(1, MAX_ATTRIBUTE_GROUPBY + 1)
            if self.env.context.get("groupby_attribute_id_%d" % s)
        ]
        if not all_requested:
            return None

        already_used = set()
        for leaf in domain:
            if (
                isinstance(leaf, (list, tuple))
                and len(leaf) == 3
                and leaf[0] == "product_template_attribute_value_ids"
                and leaf[1] == "in"
                and leaf[2]
            ):
                ptavs = self.env["product.template.attribute.value"].browse(leaf[2])
                for ptav in ptavs:
                    already_used.add(ptav.attribute_id.id)

        return next((aid for aid in all_requested if aid not in already_used), None)

    @api.model
    def _build_pav_map(self, attribute_id, template_ids):
        ptavs = self.env["product.template.attribute.value"].search(
            [
                ("attribute_id", "=", attribute_id),
                ("product_tmpl_id", "in", template_ids),
            ],
            order="product_attribute_value_id",
        )

        pav_map = {}
        for ptav in ptavs:
            pav = ptav.product_attribute_value_id
            if pav.id not in pav_map:
                pav_map[pav.id] = {
                    "pav": pav,
                    "ptav_ids": [],
                    "sequence": pav.sequence,
                }
            pav_map[pav.id]["ptav_ids"].append(ptav.id)

        return pav_map

    @api.model
    def _build_attribute_groups(self, field_name, domain, pav_map, remaining_groupby):
        def _sub_context(remaining_groupby):
            ctx = {"group_by": remaining_groupby}
            for s in range(1, MAX_ATTRIBUTE_GROUPBY + 1):
                val = self.env.context.get("groupby_attribute_id_%d" % s)
                if val:
                    ctx["groupby_attribute_id_%d" % s] = val
            return ctx

        res = []
        for data in pav_map.values():
            value_domain = list(domain) + [
                ("product_template_attribute_value_ids", "in", data["ptav_ids"])
            ]
            count = self.search_count(value_domain)
            if count == 0:
                continue
            res.append(
                {
                    field_name: (data["pav"].id, data["pav"].name),
                    "%s_count" % field_name: count,
                    "__domain": value_domain,
                    "__context": _sub_context(remaining_groupby),
                    "__fold": False,
                    "_sequence": data["sequence"],
                }
            )
        return res

    @api.model
    def _append_undefined_group(
        self, res, field_name, domain, pav_map, remaining_groupby
    ):
        all_ptav_ids = [
            ptav_id for data in pav_map.values() for ptav_id in data["ptav_ids"]
        ]
        undefined_domain = list(domain) + [
            ("product_template_attribute_value_ids", "not in", all_ptav_ids)
        ]
        undefined_count = self.search_count(undefined_domain)
        if undefined_count == 0:
            return

        sub_context = {"group_by": remaining_groupby}
        for s in range(1, MAX_ATTRIBUTE_GROUPBY + 1):
            val = self.env.context.get("groupby_attribute_id_%d" % s)
            if val:
                sub_context["groupby_attribute_id_%d" % s] = val

        res.append(
            {
                field_name: (False, "Undefined"),
                "%s_count" % field_name: undefined_count,
                "__domain": undefined_domain,
                "__context": sub_context,
                "__fold": False,
                "_sequence": 9999,
            }
        )

    @api.model
    def _sort_and_clean_groups(self, res, field_name, sort_order):
        if sort_order == "sequence":
            res.sort(key=lambda r: (r["_sequence"], r[field_name][1] or ""))
        else:
            res.sort(key=lambda r: r[field_name][1] or "")
        for group in res:
            del group["_sequence"]

    @api.model
    def _get_attribute_groups(self, slot, domain, groupby_list):
        field_name = "attribute_group_by_%d" % slot

        if field_name not in groupby_list:
            return None

        attribute_id = self._resolve_attribute_id(slot, domain)
        if not attribute_id:
            return None

        template_ids = self.search(domain).mapped("product_tmpl_id").ids
        if not template_ids:
            return []

        remaining_groupby = [g for g in groupby_list if g != field_name]
        pav_map = self._build_pav_map(attribute_id, template_ids)

        res = self._build_attribute_groups(
            field_name, domain, pav_map, remaining_groupby
        )
        self._append_undefined_group(
            res, field_name, domain, pav_map, remaining_groupby
        )

        sort_order = self.env.company.product_groupby_attribute_sort or "sequence"
        self._sort_and_clean_groups(res, field_name, sort_order)

        return res

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        groupby_list = groupby if isinstance(groupby, list) else [groupby]
        fields_to_check = groupby_list[:1] if lazy else groupby_list
        for field_name in fields_to_check:
            for slot in range(1, MAX_ATTRIBUTE_GROUPBY + 1):
                if field_name == "attribute_group_by_%d" % slot:
                    result = self._get_attribute_groups(slot, domain, groupby_list)
                    if result is not None:
                        return result
                    break

        result = super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )

        attr_ctx = {
            "groupby_attribute_id_%d"
            % i: self.env.context.get("groupby_attribute_id_%d" % i)
            for i in range(1, MAX_ATTRIBUTE_GROUPBY + 1)
            if self.env.context.get("groupby_attribute_id_%d" % i)
        }
        if attr_ctx:
            for group in result:
                group_ctx = dict(group.get("__context") or {})
                group_ctx.update(attr_ctx)
                group["__context"] = group_ctx

        return result
