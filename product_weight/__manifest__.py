# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Weight Calculation",
    "version": "14.0.1.0.0",
    "author": "Savoir-faire Linux,Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Warehouse",
    "summary": "Allows to calculate products weight from its components.",
    "depends": ["mrp"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/product_weight_update_view.xml",
        "views/product_view.xml",
    ],
    "installable": True,
}
