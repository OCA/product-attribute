# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Attribute Model Link",
    "summary": "Use any model records as product attribute values",
    "version": "16.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product_attribute_archive"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_views.xml",
        "wizards/linked_record_wizard_view.xml",
    ],
}
