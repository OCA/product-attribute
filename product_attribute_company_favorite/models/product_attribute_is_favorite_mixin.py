from odoo import api, fields, models


class ProductAttributeIsFavoriteMixin(models.AbstractModel):
    _name = "product.attribute.favorite.mixin"
    _description = """Methods used both in product.attribute and
    product.attribute.value to implement is_favorite functionalities
    """

    is_favorite = fields.Boolean(
        string="Favorite",
        company_dependent=True,
        default=True,
        help="If checked, this record can be linked to a product template.",
    )

    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        args += [("is_favorite", "=", True)]
        return super()._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )

    @api.model_create_multi
    def create(self, vals_list):
        param = "product_attribute_company_favorite.%s_enable_for_all_companies" % (
            self._name.replace(".", "_")
        )
        new_record_favorite_for_all_companies = (
            self.env["ir.config_parameter"].sudo().get_param(param)
        )
        records = super().create(vals_list)
        if new_record_favorite_for_all_companies:
            company_ids = (
                self.env["res.company"].with_context(active_test=False).search([]).ids
            )
            for record in records:
                for company_id in company_ids:
                    contextual_record = record.with_company(company_id)
                    contextual_record.is_favorite = record.is_favorite
        return records
