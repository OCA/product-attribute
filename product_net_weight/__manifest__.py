# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Products - Net Weight",
    "summary": "Add 'Net Weight' on product models",
    "version": "15.0.2.0.0",
    "category": "Product",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "views/view_product_product.xml",
        "views/view_product_template.xml",
    ],
    "demo": [
        "demo/product_product.xml",
    ],
    "images": [
        "static/description/product_product_form.png",
    ],
    "installable": True,
}
