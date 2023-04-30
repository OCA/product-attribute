# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Profile",
    "version": "15.0.1.0.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "summary": "Allow to configure a product in 1 click",
    "category": "product",
    "development_status": "Production/Stable",
    "depends": ["sale_management"],
    "website": "https://github.com/OCA/product-attribute",
    "data": [
        "security/group.xml",
        "views/product_view.xml",
        "views/config_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/profile_demo.xml"],
    "installable": True,
    "license": "AGPL-3",
    "maintainers": ["bealdav", "sebastienbeau", "kevinkhao"],
}
