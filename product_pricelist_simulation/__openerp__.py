# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Pricelist Simulation",
    "summary": "Simulate the product price for all pricelists",
    "version": "9.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product",],
    "data": [
        "views/product_view.xml",
        "views/pricelist_view.xml",
        "security/ir.model.access.csv",
    ],
}
