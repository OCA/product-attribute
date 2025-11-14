# Copyright 2023 Camptocamp SA
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Product Variant Route MTO",
    "summary": "Allow to individually set variants as MTO",
    "version": "18.0.1.0.1",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "maintainers": ["mmequignon", "jbaudoux"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": ["product_route_mto"],
    "data": ["views/product_product.xml"],
}
