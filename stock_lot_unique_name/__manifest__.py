# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

{
    "name": "Stock Lot Unique Name",
    "summary": "Refuse a lot or serial number another product already holds",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["stock"],
    "data": [
        "security/res_groups.xml",
    ],
    "post_init_hook": "post_init_hook",
}
