{
    "name": "Product Attribute Value Menu",
    "summary": """Product attributes values tree and form. Import attribute values.""",
    "version": "15.0.1.1.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Ilyas, Ooops404, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "category": "Stock",
    "depends": ["sale_stock"],
    "data": [
        "views/product_template_attribute_value_views.xml",
        "views/product_attribute_value_views.xml",
    ],
    "installable": True,
    "application": False,
}
