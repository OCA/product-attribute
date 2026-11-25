# Copyright 2026 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Kévin Roche <kevin.roche@akretion.com>

{
    "name": "Product Supplierinfo Incoterm Group",
    "summary": "Glue module between product_supplierinfo_incoterm "
    "and product_supplierinfo_group",
    "version": "18.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainer": ["kev-roche"],
    "installable": True,
    "depends": [
        "product_supplierinfo_incoterm",
        "product_supplierinfo_group",
    ],
    "data": ["views/product_supplierinfo_group.xml"],
}
