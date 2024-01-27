# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Pricelist Direct Print",
    "summary": "Print price list from menu option, product templates, "
    "products variants or price lists",
    "version": "15.0.1.3.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sale", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "views/report_product_pricelist.xml",
        # 'mail_template_data' has to be after 'report_product_pricelist'
        "data/mail_template_data.xml",
        "report/product_pricelist_xlsx.xml",
        "wizards/product_pricelist_print_view.xml",
    ],
}
