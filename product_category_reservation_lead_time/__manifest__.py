{
    "name": "Product Category Reservation Lead Time",
    "version": "16.0.1.0.0",
    "category": "Other",
    "author": "FactorLibre, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "summary": "Plazo de reserva (dias) por categoria de producto, heredable y por compañia",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_reservation_rule_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
}
