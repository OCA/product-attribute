from odoo import api, fields, models
from odoo.osv import expression


class ProductSticker(models.Model):
    _name = "product.sticker"
    _description = "Product Sticker"
    _inherit = ["image.mixin"]
    _order = "sequence, id"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s.env.company,
    )
    sequence = fields.Integer(default=10, index=True)
    name = fields.Char(required=True, translate=True)
    image_1920 = fields.Image(required=True)
    image_64 = fields.Image(
        related="image_1920",
        max_width=64,
        max_height=64,
        store=True,
        string="Small Image",
    )
    image_size = fields.Selection(
        selection=[
            ("64", "64x64 px"),
            ("128", "128x128 px"),
            ("256", "256x256 px"),
            ("512", "512x512 px"),
            ("1024", "1024x1024 px"),
            ("1920", "1920x1920 px"),
        ],
        required=True,
        default="64",
        help="Max size of the Sticker. Max Width x Max Height",
    )
    available_model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Available Models",
        help="Models where this sticker is available. Empty means all models.",
    )
    product_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Category",
        ondelete="cascade",
    )
    product_attribute_id = fields.Many2one(
        comodel_name="product.attribute",
        string="Attribute",
        ondelete="cascade",
    )
    product_attribute_value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Attribute value",
        ondelete="cascade",
        domain="[('attribute_id', '=', product_attribute_id)]",
    )
    show_sticker_note = fields.Boolean(
        string="Sticker Note",
        help="If checked, the note will be displayed with the sticker",
    )
    # You can use <t-esc="sticker.note" style="white-space: pre;" /> to display
    # break lines in reports
    note = fields.Text(
        translate=True,
        help="Used to display a note with the sticker",
    )

    def get_image(self):
        """Get the image of the sticker"""
        self.ensure_one()
        return getattr(self, f"image_{self.image_size}", self.image_64)

    @api.onchange("product_attribute_id")
    def _onchange_product_attribute_id(self):
        pav_dom = []
        if self.product_attribute_id:
            pav_dom = [("attribute_id", "=", self.product_attribute_id.id)]

        pav_value = False
        if self.product_attribute_value_id in self.product_attribute_id.value_ids:
            pav_value = self.product_attribute_value_id.id
        return {
            "domain": {"product_attribute_value_id": pav_dom},
            "value": {"product_attribute_value_id": pav_value},
        }

    @api.onchange("product_attribute_value_id")
    def _onchange_product_attribute_value_id(self):
        if self.product_attribute_value_id:
            return {
                "value": {
                    "product_attribute_id": (
                        self.product_attribute_value_id.attribute_id.id
                    ),
                },
            }
        return {}

    @api.model
    def _build_sticker_domain_company(self):
        """Build domain for companies"""
        return expression.OR(
            [
                [("company_id", "=", False)],
                [
                    (
                        "company_id",
                        "in",
                        self.env.context.get(
                            "allowed_company_ids", self.env.company.ids
                        ),
                    )
                ],
            ]
        )

    @api.model
    def _build_sticker_domain_category(self, categories=None):
        """Build domain for categories"""
        category_domain = [("product_category_id", "=", False)]
        if categories:
            category_domain = expression.OR(
                [
                    category_domain,
                    [("product_category_id", "child_of", categories.ids)],
                ]
            )
        return category_domain

    @api.model
    def _build_sticker_domain_attributes(self, attributes=None, attribute_values=None):
        """Build domain for attributes and attribute values"""
        attribute_domain = [
            ("product_attribute_id", "=", False),
            ("product_attribute_value_id", "=", False),
        ]
        if attribute_values:
            full_attributes = attributes | attribute_values.mapped("attribute_id")
            attribute_domain = expression.OR(
                [
                    attribute_domain,
                    expression.OR(
                        [
                            [
                                (
                                    "product_attribute_value_id",
                                    "in",
                                    attribute_values.ids,
                                )
                            ],
                            expression.AND(
                                [
                                    [("product_attribute_value_id", "=", False)],
                                    [
                                        (
                                            "product_attribute_id",
                                            "in",
                                            full_attributes.ids,
                                        )
                                    ],
                                ]
                            ),
                        ]
                    ),
                ]
            )
        elif attributes:
            attribute_domain = expression.OR(
                [
                    attribute_domain,
                    expression.AND(
                        [
                            [("product_attribute_value_id", "=", False)],
                            expression.OR(
                                [
                                    [("product_attribute_id", "in", attributes.ids)],
                                    [("product_attribute_id", "=", False)],
                                ]
                            ),
                        ]
                    ),
                ]
            )
        return attribute_domain

    def _get_product_sticker_domain(
        self,
        categories=None,
        attributes=None,
        attribute_values=None,
    ):
        company_domain = self._build_sticker_domain_company()
        category_domain = self._build_sticker_domain_category(categories)
        attribute_domain = self._build_sticker_domain_attributes(
            attributes, attribute_values
        )
        return expression.AND([company_domain, category_domain, attribute_domain])

    @api.model
    def _get_stickers(self, products, extra_domain=None):
        """Get stickers for given categories, attributes, attribute values and models"""
        product_templates = products.product_tmpl_id
        no_variant_attribute_lines = product_templates.attribute_line_ids.filtered(
            lambda al: al.attribute_id.create_variant == "no_variant"
        )
        pp_pavs = products.product_template_variant_value_ids.product_attribute_value_id
        product_sticker_domain = self._get_product_sticker_domain(
            categories=products.categ_id,
            attributes=no_variant_attribute_lines.attribute_id | pp_pavs.attribute_id,
            attribute_values=no_variant_attribute_lines.value_ids | pp_pavs,
        )
        return self.search(expression.AND([product_sticker_domain, extra_domain or []]))
