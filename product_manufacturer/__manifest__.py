# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Manufacturer",
    "version": "16.0.1.0.0",
    "summary": "Adds manufacturers and attributes on the product view.",
    "website": "https://github.com/OCA/product-attribute",
    "author": "OpenERP SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Product",
    "external_dependencies": {"python": ["openupgradelib"]},
    "depends": ["product"],
    "data": ["views/product_manufacturer_view.xml"],
    "auto_install": False,
    "installable": True,
}
