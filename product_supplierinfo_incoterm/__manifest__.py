# Copyright 2026 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Kévin Roche <kevin.roche@akretion.com>

{
    "name": "Product Supplierinfo Incoterm",
    "summary": "Add an incoterm on vendor pricelists, defaulted from the vendor",
    "version": "18.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "maintainer": ["kev-roche"],
    "depends": ["purchase_partner_incoterm"],
    "data": ["views/product_supplierinfo.xml"],
}
