# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Stock Availability",
    "summary": """This module allows to store the supplier stock level (indicator)
    of a particular product""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["rousseldenis"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/security.xml",
        "views/product_supplierinfo.xml",
    ],
}
