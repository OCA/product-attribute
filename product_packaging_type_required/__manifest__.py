# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging Type Required",
    "version": "14.0.1.1.0",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Product Packaging Type Required",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "maintainers": ["simahawk", "dcrier"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product", "product_packaging_type"],
    "data": ["data/cron.xml", "views/product_packaging_type_view.xml"],
    "installable": True,
    "auto_install": False,
}
