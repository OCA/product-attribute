# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Profile",
    "version": "12.0.2.0.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "summary": "Allow to configure a product in 1 click",
    "category": "product",
    "depends": ["sale_management"],
    "website": "https://github.com/oca/product-attribute",
    "data": [
        "security/group.xml",
        "views/product_view.xml",
        "views/config_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "license": "AGPL-3",
    "maintainers": ["bealdav", "sebastienbeau", "kevinkhao"],
}
