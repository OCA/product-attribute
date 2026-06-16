# © 2021  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product life period",
    "version": "14.0.1.0.0",
    "author": "Acsone SA/NV, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_state", "sale"],
    "data": [
        "views/product_life_period_views.xml",
        "views/product_template.xml",
        "security/ir.model.access.csv",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
