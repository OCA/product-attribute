# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Pricelist Direct Print (XLSX)",
    "summary": "Print price list in XLSX format",
    "version": "17.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product_pricelist_direct_print", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "report/product_pricelist_xlsx.xml",
        "wizards/product_pricelist_print_view.xml",
    ],
}
