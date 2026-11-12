# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Customer Info Company Group",
    "summary": "Fall back to the parent company's or company group's customer info",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Sales/Sales",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        # OCA/partner-contact
        "base_partner_company_group",
        # OCA/product-attribute
        "product_customerinfo",
    ],
    "installable": True,
}
