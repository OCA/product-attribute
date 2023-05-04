from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    new_attribute_favorite_for_all_companies = fields.Boolean(
        config_parameter=(
            "product_attribute_company_favorite."
            "product_attribute_enable_for_all_companies"
        ),
        string="Set new attribute as favorite for all companies",
        help="""When a new attribute is created,
        set it as favorite for all companies.
        Otherwise it is only set as favorite for the user's current company""",
    )

    new_attribute_value_favorite_for_all_companies = fields.Boolean(
        config_parameter=(
            "product_attribute_company_favorite."
            "product_attribute_value_enable_for_all_companies"
        ),
        string="Set new attributes value as favorite for all companies",
        help="""When a new attribute value is created,
        set it as favorite for all companies.
        Otherwise it is only set as favorite for the user's current company""",
    )
