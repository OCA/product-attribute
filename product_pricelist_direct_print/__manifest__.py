# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Pricelist Direct Print",
    "summary": "Print price list from menu option, product templates, "
    "products variants or price lists",
    "version": "13.0.3.1.1",
    "category": "Product",
    "website": "https://www.github.com/OCA/product-attribute",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sale", "report_xlsx"],
    "data": [
        "views/report_product_pricelist.xml",
        # 'mail_template_data' has to be after 'report_product_pricelist'
        "data/mail_template_data.xml",
        "report/product_pricelist_xlsx.xml",
        "wizards/product_pricelist_print_view.xml",
    ],
}
