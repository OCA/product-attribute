# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product uom reference",
    "version": "18.0.1.0.0",
    "category": "Product",
    "summary": "Configure reference unit of measurement",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_uom_reference_views.xml",
        "views/product_template_views.xml",
        "views/product_uom_reference_ratio_menu_views.xml",
        "report/product_product_templates.xml",
    ],
}
