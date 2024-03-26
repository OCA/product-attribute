# Copyright 2017 ACSONE SA/NV
# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_default_tag_propagation(self):
        return "tmpl2prod"

    tag_ids = fields.Many2many(
        comodel_name="product.template.tag",
        string="Tags",
        relation="product_template_product_tag_rel",
        column1="product_tmpl_id",
        column2="tag_id",
        compute="_compute_tag_ids",
        inverse="_inverse_tag_ids",
        store=True,
    )
    tag_propagation = fields.Selection(
        string="Tag Propagation",
        selection=[
            ("tmpl2prod", "From template to variants"),
            ("prod2tmpl", "From variants to template"),
        ],
        default=lambda self: self._get_default_tag_propagation(),
        required=True,
        help="Defines how tags are propagated among templates and variants.\n"
        "- From template to variants: variants' tags are read-only, and copied"
        " from their template\n"
        "- From variants to template: template's tags are read-only, and are"
        " defined as a full list of all its variants' tags\n",
    )

    @api.depends("product_variant_ids.tag_ids", "tag_propagation")
    def _compute_tag_ids(self):
        # Update only templates whose tags are read from variants
        for tmpl in self.filtered(lambda x: x.tag_propagation == "prod2tmpl"):
            tmpl.tag_ids = tmpl.product_variant_ids.tag_ids

    def _inverse_tag_ids(self):
        # Update only variants whose tags are read from templates
        for tmpl in self.filtered(lambda x: x.tag_propagation == "tmpl2prod"):
            tmpl.product_variant_ids.tag_ids = tmpl.tag_ids
