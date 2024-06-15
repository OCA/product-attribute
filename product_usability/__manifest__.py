# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product - Missing Menus and Groups",
    "version": "16.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "summary": "Adds missing menu entries for Product module and"
    " adds extra groups to fine-tune access rights",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": ["product"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "installable": True,
}
