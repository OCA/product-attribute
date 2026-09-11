# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Document Type",
    "summary": "Classify product documents by a translatable, configurable type",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product",
    "depends": [
        "product",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/product_document_type_security.xml",
        "data/product_document_type_data.xml",
        "views/product_document_type_views.xml",
        "views/product_document_views.xml",
    ],
    "installable": True,
}
