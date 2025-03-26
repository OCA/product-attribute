# Copyright (C) 2025  Renato Lima - Akretion
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "UOM Alias",
    "summary": """Adds alias for UOM""",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "development_status": "Beta",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["renatonlima"],
    "depends": ["uom"],
    "data": [
        "security/ir.model.access.csv",
        "views/uom_uom.xml",
        "views/uom_category.xml",
    ],
}
