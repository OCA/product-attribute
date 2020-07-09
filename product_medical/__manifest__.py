# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Medical",
    "summary": "Base  structure to handle medical products",
    "version": "13.0.1.1.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product"],
    "data": [
        "data/medical_data.xml",
        "security/ir.model.access.csv",
        "views/product_template.xml",
    ],
    "installable": True,
}
