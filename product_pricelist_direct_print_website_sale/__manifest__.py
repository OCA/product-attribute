# Copyright 2020 Tecnativa - Carlos Roca
# Copyright 2023 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Pricelist Print Website Sale",
    "summary": "Extend Product Pricelist Direct Print for filter by public"
    " categories",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "maintainers": ["CarlosRoca13"],
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product_pricelist_direct_print",
        "website_sale",
        "product_pricelist_direct_print_xlsx",
    ],
    "data": ["wizards/product_pricelist_print_view.xml"],
}
