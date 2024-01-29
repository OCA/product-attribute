# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateTag(models.Model):
    _name = "product.template.tag"
    _description = "Product Tag"
    _order = "sequence, name"
    _parent_store = True

    name = fields.Char(required=True, translate=True)
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
    parent_id = fields.Many2one("product.template.tag", index=True, ondelete="cascade")
    child_ids = fields.One2many("product.template.tag", "parent_id")
    parent_path = fields.Char(index=True)

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

    def name_get(self):
        res = []
        for tag in self:
            names = []
            current = tag
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((tag.id, " / ".join(reversed(names))))
        return res

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        if name:
            args = [("name", operator, name.split(" / ")[-1])] + list(args or [])
        return super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        if not self._check_recursion("parent_id"):
            raise ValidationError(_("Tags cannot be recursive."))
