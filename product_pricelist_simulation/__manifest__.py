# Copyright (C) 2021-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Margins per Pricelist",
    "version": "12.0.1.0.0",
    "category": "Account",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["sale"],
    "data": [
        "views/view_product_template.xml",
        "wizards/wizard_preview_pricelist_margin.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_product.xml",
        "demo/product_pricelist.xml",
    ],
    "installable": True,
}
