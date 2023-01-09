# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Products - Drained Weight",
    "summary": "Add 'Drained Weight' on product models",
    "version": "15.0.1.0.0",
    "category": "Product",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product_net_weight"],
    "data": [
        "views/view_product_product.xml",
        "views/view_product_template.xml",
    ],
    "installable": True,
}
