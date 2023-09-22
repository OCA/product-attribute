# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Group",
    "version": "14.0.2.0.3",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["purchase"],
    "data": [
        "views/product.xml",
        "views/supplierinfo_group.xml",
        "views/templates.xml",
        "views/assets.xml",
        "security/ir.model.access.csv",
        "security/supplierinfo_group_security.xml",
    ],
    "pre_init_hook": "fill_required_group_id_column",
}
