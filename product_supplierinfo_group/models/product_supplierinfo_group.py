# Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# Copyright (C) 2020-Today Akretion (http://www.akretion.com)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSupplierinfoGroup(models.Model):
    _name = "product.supplierinfo.group"
    _description = "Supplierinfo group"
    _order = "sequence, id"

    product_tmpl_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade"
    )
    supplierinfo_ids = fields.One2many("product.supplierinfo", "group_id")
    product_id = fields.Many2one(
        "product.product",
        "Product Variant",
        help="If not set, the vendor price will apply to all "
        "variants of this product.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Vendor",
        ondelete="cascade",
        required=True,
        help="Vendor of this product",
    )
    product_name = fields.Char(
        "Vendor Product Name",
        help="This vendor's product name will be used when printing "
        "a request for quotation. Keep empty to use the internal one.",
    )
    product_code = fields.Char(
        "Vendor Product Code",
        help="This vendor's product code will be used when printing "
        "a request for quotation. Keep empty to use the internal one.",
    )
    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Assigns the priority to the list of product vendor.",
    )
    unit_price_note = fields.Html(
        compute="_compute_unit_price_note", string="Unit Prices (Min. Qty / Price)"
    )
    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company.id, index=1
    )
    has_multiple_variants = fields.Boolean(compute="_compute_has_variants")

    _sql_constraints = [
        (
            "product_partner_company_uniq",
            "unique(product_tmpl_id, product_id, company_id, partner_id)",
            "A supplier group already exist for the partner, product and company",
        )
    ]

    @api.depends("product_tmpl_id")
    def _compute_has_variants(self):
        for rec in self:
            rec.has_multiple_variants = len(rec.product_tmpl_id.product_variant_ids) > 1

    @api.depends("supplierinfo_ids")
    def _compute_unit_price_note(self):
        for rec in self:
            if len(rec.supplierinfo_ids) == 0:
                rec.unit_price_note = "-"
            else:
                sorted_supinfos = rec.supplierinfo_ids.sorted(key=lambda r: r.min_qty)
                vals = {"supinfos": [rec for rec in sorted_supinfos]}
                rec.unit_price_note = self.env["ir.qweb"]._render(
                    "product_supplierinfo_group.table_price_note", vals
                )
