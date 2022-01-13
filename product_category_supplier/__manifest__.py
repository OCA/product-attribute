# Copyright 2022 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Category Supplier",
    "summary": "Add supplier Type and supplier_categ_id on product Categories",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "product_category_type",
        "purchase",
    ],
    "data": ["views/product_template.xml"],
}
