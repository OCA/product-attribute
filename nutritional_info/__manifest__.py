# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Nutritional Info",
    "summary": "Nutritional information.",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Technical Settings",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["CarlosRoca13"],
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "report/report_nutritional_info.xml",
        "security/ir.model.access.csv",
        "views/nutritional_type_view.xml",
        "views/product_views.xml",
        "views/res_config_settings_view.xml",
    ],
    "application": False,
    "installable": True,
    "assets": {
        "web.report_assets_common": [
            "nutritional_info/static/src/scss/nutrition_table_style.scss",
        ]
    },
}
