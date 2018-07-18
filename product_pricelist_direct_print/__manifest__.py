# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Direct Print",
    "summary": "Print price list from menu option, product templates, "
               "products variants or price lists",
    "version": "11.0.1.0.0",
    "category": "Product",
    "website": "https://www.github.com/OCA/product-attribute",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "data/pricelist_send_action.xml",
        "views/report_product_pricelist.xml",
        "wizards/product_pricelist_print_view.xml",
        "data/mail_template_data.xml",
    ],
}
