# Copyright 2023 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy<raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCatalog(models.Model):
    _name = "product.catalog"
    _description = "Product Catalog"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    product_assortment_id = fields.Many2one(
        "ir.filters", domain="[['is_assortment', '=', True]]"
    )

    assortment_domain = fields.Binary(
        compute="_compute_assortment_domain", readonly=True
    )

    pp_candidate_member_ids = fields.Many2many(
        "product.product",
        compute="_compute_pp_candidate_to_add_or_remove_member_ids",
        store=False,
        readonly=True,
    )
    pp_effective_member_ids = fields.Many2many(
        "product.product",
        relation="pp_product_catalog_rel",
        column1="product_id",
        column2="catalog_id",
    )
    pp_to_remove_member_ids = fields.Many2many(
        "product.product",
        compute="_compute_pp_candidate_to_add_or_remove_member_ids",
        store=False,
        readonly=True,
    )

    def _compute_assortment_domain(self):
        for rec in self:
            rec.assortment_domain = rec.product_assortment_id._get_eval_domain()

    def _add_all_candidates(self):
        for rec in self:
            toadd = set(rec.pp_candidate_member_ids.ids)
            existing = set(rec.pp_effective_member_ids.ids)
            rec.pp_effective_member_ids = [(6, 0, list(existing + toadd))]

    def _remove_all_candidates(self):
        for rec in self:
            torm = set(rec.pp_to_remove_member_ids.ids)
            existing = set(rec.pp_effective_member_ids.ids)
            rec.pp_effective_member_ids = [(6, 0, list(existing - torm))]

    @api.depends("pp_effective_member_ids", "product_assortment_id")
    def _compute_pp_candidate_to_add_or_remove_member_ids(self):
        for rec in self:
            if not rec.product_assortment_id:
                rec.pp_candidate_member_ids = [(5, 0, 0)]  # clear
                rec.pp_to_remove_member_ids = [(5, 0, 0)]  # clear
                continue

            domain = rec.product_assortment_id._get_eval_domain()
            target = set(self.env["product.product"].search(domain).ids)
            effective = set(rec.pp_effective_member_ids.ids)

            candidates_ids = target - effective
            to_remove_ids = effective - target
            if candidates_ids:
                rec.pp_candidate_member_ids = [(6, 0, candidates_ids)]  # set
            else:
                rec.pp_candidate_member_ids = [(5, 0, 0)]  # clear

            if to_remove_ids:
                rec.pp_to_remove_member_ids = [(6, 0, to_remove_ids)]  # set
            else:
                rec.pp_to_remove_member_ids = [(5, 0, 0)]  # clear
