# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product State Shortage",
    "summary": """Enables to declare a product state as a "shortage" state.
    Such a state will automatically resolve to default state whenever new stock
    is received for this product avoiding the need for manual intervention""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_state", "stock"],
    "data": ["views/product_state.xml", "data/ir_cron_data.xml"],
    "demo": [],
}
