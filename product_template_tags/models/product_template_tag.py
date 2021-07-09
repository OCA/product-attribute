# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplateTag(models.Model):
    _name = "product.template.tag"
    _description = "Product Tag"
    _order = "sequence, name"

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
    products_count = fields.Integer(
        string="# of Products", compute="_compute_products_count"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name, company_id)",
            "Tag name must be unique inside a company",
        ),
    ]

    @api.depends("product_tmpl_ids")
    def _compute_products_count(self):
        tag_id_product_count = {}
        if self.ids:
            self.env.cr.execute(
                """SELECT tag_id, COUNT(*)
                FROM product_template_product_tag_rel
                WHERE tag_id IN %s
                GROUP BY tag_id""",
                (tuple(self.ids),),
            )
            tag_id_product_count = dict(self.env.cr.fetchall())
        for rec in self:
            rec.products_count = tag_id_product_count.get(rec.id, 0)
