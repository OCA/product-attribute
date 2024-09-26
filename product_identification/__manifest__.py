# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Product Identification",
    "summary": "Product Identification",
    "version": "17.0.1.0.0",
    "category": "Product",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "data/ir_cron.xml",
        "data/email_template_data.xml",
        "security/ir.model.access.csv",
        "views/product_identification_category_view.xml",
        "views/product_identification_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
}
