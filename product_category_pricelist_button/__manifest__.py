# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

{
    "name": "Product category pricelist button",
    "summary": """
        Adds a smart button to product categories linking to associated price rules.
    """,
    "author": "Solvos,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "version": "18.0.1.1.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "views/product_category_views.xml",
    ],
    "installable": True,
}
