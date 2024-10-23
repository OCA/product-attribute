# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product - UoM Measure Type",
    "version": "17.0.1.0.0",
    "category": "Product",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/view_uom_category.xml",
        "views/view_uom_uom.xml",
        "views/view_product_template.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
