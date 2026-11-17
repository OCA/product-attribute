from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(
        selection_add=[
            ("product_tag", "Product Tag"),
        ],
        ondelete={"product_tag": "set default"},
    )

    display_applied_on = fields.Selection(
        selection_add=[
            ("product_tag", "Product Tag"),
        ],
        ondelete={"product_tag": "set default"},
    )

    product_tag_id = fields.Many2one(
        comodel_name="product.tag",
        string="Tags",
        ondelete="cascade",
        help="Specify product tag if this rule only applies to products\
        belonging to this tag. Keep empty otherwise.",
    )

    @api.depends(
        "applied_on", "product_tag_id", "categ_id", "product_tmpl_id", "product_id"
    )
    def _compute_name(self):
        res = super()._compute_name()
        for item in self:
            if item.product_tag_id and item.applied_on == "product_tag":
                item.name = _("Tag: %s", item.product_tag_id.display_name)
        return res

    @api.constrains("product_id", "product_tmpl_id", "categ_id", "product_tag_id")
    def _check_product_consistency(self):
        for item in self:
            if item.applied_on == "product_tag" and not item.product_tag_id:
                raise ValidationError(
                    _(
                        "Please specify the tag for which this rule\
                      should be applied"
                    )
                )
        return super()._check_product_consistency()

    @api.onchange("display_applied_on")
    def _onchange_display_applied_on(self):
        tag_items = self.filtered(lambda item: item.display_applied_on == "product_tag")
        for item in tag_items:
            if item.product_tag_id:
                item.update(
                    dict(
                        product_id=None,
                        product_tmpl_id=None,
                        applied_on="product_tag",
                        product_uom=None,
                    )
                )
            else:
                item.applied_on = "3_global"
        return super(PricelistItem, self - tag_items)._onchange_display_applied_on()

    @api.onchange("product_id", "product_tmpl_id", "categ_id", "product_tag_id")
    def _onchange_rule_content(self):
        res = super()._onchange_rule_content()
        if not self.env.context.get("default_applied_on", False):
            tag_rules = self.filtered(
                lambda item: (
                    item.product_tag_id and item.display_applied_on == "product_tag"
                )
            )
            tag_rules.update({"applied_on": "product_tag"})
        return res

    # === CRUD METHODS ===#

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("applied_on") and values.get("product_tag_id"):
                values["applied_on"] = "product_tag"
            # Ensure item consistency for later searches.
            if values.get("applied_on") == "product_tag":
                values.update(
                    dict(product_id=None, product_tmpl_id=None, categ_id=None)
                )
        return super().create(vals_list)

    def write(self, values):
        if values.get("applied_on", False):
            # Ensure item consistency for later searches.
            applied_on = values["applied_on"]
            if applied_on == "product_tag":
                values.update(
                    dict(product_id=None, product_tmpl_id=None, categ_id=None)
                )
        return super().write(values)

    # === BUSINESS METHODS ===#

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        product.ensure_one()
        res = super()._is_applicable_for(product, qty_in_product_uom)

        if res and self.applied_on == "product_tag":
            tags = (
                product.product_tag_ids
                if product._name == "product.template"
                else product.all_product_tag_ids
            )
            res = self.product_tag_id in tags
        return res
