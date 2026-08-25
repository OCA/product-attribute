{
    "name": "Product Class",
    "version": "19.0.1.1.1",
    "summary": "Product classification and attribute constraints",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product", "stock", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_class_views.xml",
        "views/product_attribute_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "maintainers": ["Ricardoalso", "ivantodorovich"],
}
