# Copyright 2020 Lorenzo Battistini @ TAKOBI
# Copyright 2020 Andrea Piovesana @ Openindustry.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product model viewer",
    "summary": "3D model viewer for products",
    "version": "14.0.1.0.1",
    "development_status": "Beta",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "TAKOBI, Openindustry.it, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "depends": [
        "web_widget_model_viewer",
        "product",
    ],
    "data": [
        "views/product_views.xml",
    ],
    "demo": [
        "data/product_demo.xml",
    ],
    "application": False,
    "installable": True,
}
