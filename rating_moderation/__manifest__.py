# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Rating moderation",
    "summary": """Rating moderation module""",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Productivity",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["rating"],
    "data": ["security/res_groups.xml", "views/rating_view.xml"],
    "installable": True,
}
