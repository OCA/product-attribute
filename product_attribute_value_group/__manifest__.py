{
    "name": "Product Attribute Value Group",
    "summary": """Product Attribute Value Groups for dynamic assignment on Product Templates""",
    "version": "16.0.0.1.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Galvintec, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "category": "Stock",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_value_group_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
}
