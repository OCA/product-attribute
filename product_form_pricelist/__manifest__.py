# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "product_form_pricelist",
    "summary": "Show/edit pricelist in product form",
    "version": "14.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": " Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale",
    ],
    "data": [
        "security/res_groups.xml",
        "views/product_template_view.xml",
        "views/product_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "demo": [],
    "qweb": [],
}
