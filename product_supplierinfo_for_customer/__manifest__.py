# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015-18 Tecnativa
# Copyright 2017-18 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Supplierinfo for Customers",
    "summary": "Allows to define prices for customers in the products",
    "version": "16.0.1.0.4",
    "development_status": "Production/Stable",
    "author": "AvanzOSC, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
    ],
    "demo": ["demo/product_demo.xml"],
    "installable": True,
}
