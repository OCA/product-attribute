# Copyright 2019, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product UoM - Use Type",
    "summary": "Define UoM for Sale and / or for Purchase purpose",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "license": "AGPL-3",
    "depends": ["product", "uom"],
    "data": ["views/view_product_uom.xml"],
    "demo": [
        "demo/product_uom.xml",
        "demo/product_template.xml",
        "demo/res_groups.xml",
    ],
    "installable": True,
}
