# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Medical",
    "summary": "Base structure to handle medical products",
    "version": "18.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product"],
    "data": [
        "data/medical_data.xml",
        "data/in_vitro_diagnostic_data.xml",
        "data/medicine_category_data.xml",
        "data/ppe_category_data.xml",
        "security/ir.model.access.csv",
        "views/product_template.xml",
        "views/in_vitro_diagnostic.xml",
        "views/medical_class.xml",
        "views/medicine_category.xml",
        "views/ppe_category.xml",
    ],
    "installable": True,
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
}
