# Copyright 2017 ACSONE SA/NV
# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplateTag(models.Model):
    _name = "product.template.tag"
    _description = "Product Tag"
    _order = "sequence, name"

    @api.model
    def _get_default_company_id(self):
        return self.env.company

    name = fields.Char(string="Name", required=True, translate=True)
    sequence = fields.Integer(default=10)
    color = fields.Integer(string="Color Index")
    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        string="Products",
        relation="product_template_product_tag_rel",
        column1="tag_id",
        column2="product_tmpl_id",
    )
    product_tmpl_count = fields.Integer(
        string="# of Products", compute="_compute_product_tmpl_count"
    )
    product_prod_ids = fields.Many2many(
        comodel_name="product.product",
        string="Variants",
        relation="product_product_product_tag_rel",
        column1="tag_id",
        column2="product_id",
    )
    product_prod_count = fields.Integer(
        string="# of Variants", compute="_compute_product_prod_count"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self._get_default_company_id(),
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name, company_id)",
            "Tag name must be unique inside a company",
        ),
    ]

    @api.depends("product_tmpl_ids")
    def _compute_product_tmpl_count(self):
        tag_id_product_tmpl_count = {}
        if self.ids:
            self.env.cr.execute(
                """
                SELECT tag_id, COUNT(1)
                FROM product_template_product_tag_rel
                WHERE tag_id IN %s
                GROUP BY tag_id
                """,
                (tuple(self.ids),),
            )
            tag_id_product_tmpl_count = dict(self.env.cr.fetchall())
        for tag in self:
            tag.product_tmpl_count = tag_id_product_tmpl_count.get(tag.id, 0)

    @api.depends("product_prod_ids")
    def _compute_product_prod_count(self):
        tag_id_product_prod_count = {}
        if self.ids:
            self.env.cr.execute(
                """
                SELECT tag_id, COUNT(1)
                FROM product_product_product_tag_rel
                WHERE tag_id IN %s
                GROUP BY tag_id
                """,
                (tuple(self.ids),),
            )
            tag_id_product_prod_count = dict(self.env.cr.fetchall())
        for tag in self:
            tag.product_prod_count = tag_id_product_prod_count.get(tag.id, 0)
