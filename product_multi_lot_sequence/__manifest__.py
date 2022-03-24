# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Multi Lot Sequence",
    "summary": """
        Adds ability to define a multiple lot sequence from the product""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow S.L., Odoo Community Association (OCA)",
    "website": "https://www.github.com/OCA/product-attribute",
    "depends": ["stock", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_sequence_views.xml",
        "views/product_views.xml",
        "views/stock_production_lot_views.xml"
    ],
}
