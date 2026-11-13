# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Attribute Value Merge",
    "summary": "Merge duplicated attribute values without touching variants, with undo",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["carlosdauden"],
    "license": "AGPL-3",
    "development_status": "Beta",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_value_merge_views.xml",
        "views/product_attribute_views.xml",
        "wizards/product_attribute_value_merge_wizard_views.xml",
        "wizards/product_attribute_value_merge_finder_views.xml",
    ],
    "installable": True,
}
