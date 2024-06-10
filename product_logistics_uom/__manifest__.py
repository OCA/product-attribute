# Copyright 2020 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product logistics UoM",
    "summary": "Configure product weights and volume UoM",
    "version": "16.0.3.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": " Akretion, ACSONE SA/NV, Odoo Community Association (OCA)",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "views/res_config_settings.xml",
        "views/product.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
