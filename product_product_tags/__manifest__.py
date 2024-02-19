# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Product Variant Tags",
    "summary": "This addon allow to add tags on products variants",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product", "product_template_tags"],
    "data": [
        "views/product_views.xml",
        "security/product_template_tag.xml",
        "security/ir.model.access.csv",
    ],
    "maintainers": ["paoloyammouni"],
}
