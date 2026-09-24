{
    "name": "Product State Control Sale Purchase",
    "summary": """
        This module extends the functionality of the product
        state management by adding controls
        on Sales and Purchase orders confirmation based on
        the product's lifecycle state.
    """,
    "author": "Odoo Community Association (OCA), Smile",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["product_state", "sale", "purchase"],
    "data": ["views/product_state_views.xml"],
    "post_init_hook": "post_init_hook",
}
