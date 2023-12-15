{
    "name": "Product Internal Reference Generator",
    "summary": """Product template and variant reference based on sequence""",
    "author": "Ilyas, Ooops, Odoo Community Association (OCA)",
    "maintainers": ["ilyasProgrammer"],
    "license": "AGPL-3",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Sale",
    "version": "16.0.1.0.0",
    "depends": ["stock", "base_view_inheritance_extension"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/product.xml",
    ],
    "demo": ["demo/product_code_seq_demo.xml"],
    "installable": True,
    "application": False,
}
