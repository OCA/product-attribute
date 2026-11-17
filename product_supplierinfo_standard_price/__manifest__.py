# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product SupplierInfo Standard Price",
    "summary": "Product supplier easily connected to product's standard price",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["quentinDupont"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        # Odoo
        "product",
        # OCA
        "web_notify",
    ],
    "data": [
        "views/view_product_supplierinfo.xml",
    ],
    "installable": True,
}
