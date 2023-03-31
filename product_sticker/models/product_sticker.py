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
                    "product_attribute_id": self.product_attribute_value_id.attribute_id.id
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

    def _get_sticker_domains(
        self, categories=None, attributes=None, attribute_values=None
    ):
        company_domain = self._build_sticker_domain_company()
        category_domain = self._build_sticker_domain_category(categories)
        attribute_domain = self._build_sticker_domain_attributes(
            attributes, attribute_values
        )
        return [company_domain, category_domain, attribute_domain]

    @api.model
    def _get_stickers(self, categories=None, attributes=None, attribute_values=None):
        """Get stickers for given categories, attributes and attribute values"""
        sticker_domain = expression.AND(
            self._get_sticker_domains(
                categories=categories,
                attributes=attributes,
                attribute_values=attribute_values,
            )
        )
        return self.sudo().search(sticker_domain)
