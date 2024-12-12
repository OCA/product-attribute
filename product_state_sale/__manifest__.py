# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State Sale",
    "summary": """
        This module add the use of Product State in Sale""",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["product_state", "sale"],
    "data": ["security/security.xml", "views/product_state_views.xml"],
    "auto_install": True,
}
