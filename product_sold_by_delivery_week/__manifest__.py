# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product weekly sales hint",
    "summary": "Adds a field that graphically hints the weekly product sales",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["sale_stock"],
    "data": ["data/ir_cron.xml", "views/product_views.xml", "views/sale_views.xml"],
    "post_init_hook": "post_init_hook",
}
