{
    "name": "Product ABC Classification Finance",
    "summary": "Financial ABC analysis for products (cost, sale price)",
    "version": "16.0.1.0.2",
    "category": "Inventory/Inventory",
    "author": "AJamal13,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product_abc_classification_sale_stock", "sale_margin"],
    "data": [
        "security/ir.model.access.csv",
        "views/abc_finance_sale_level_history_views.xml",
        "views/abc_classification_product_level_views.xml",
        "views/abc_classification_profile.xml",
    ],
    "demo": [
        "data/abc_classification_finance_demo.xml",
    ],
    "maintainers": ["AJamal13"],
    "installable": True,
    "application": False,
}
