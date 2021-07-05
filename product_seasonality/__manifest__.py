# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product seasonality",
    "summary": "Define rules for products' seasonal availability",
    "version": "14.0.1.2.1",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Others",
    "depends": [
        # core
        "product",
    ],
    "website": "https://github.com/OCA/product-attribute",
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Views
        "views/seasonal_config.xml",
        "views/seasonal_config_line.xml",
        "views/res_company.xml",
        "views/res_partner.xml",
    ],
    "installable": True,
}
