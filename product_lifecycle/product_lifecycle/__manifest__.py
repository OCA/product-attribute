# Copyright 2019 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Product Lifecycle",
    "summary": "Manage replacement of obsolete products",
    "version": "12.0.1.0.0",
    "author": "Vauxoo",
    "website": "http://www.vauxoo.com/",
    "license": "LGPL-3",
    "category": "product",
    "depends": [
        "sale_stock",
    ],
    "data": [
        "data/ir_cron.xml",
        "views/product_view.xml",
        "views/sale_order_views.xml",
        "views/assets.xml",
    ],
    "demo": [
        "demo/replacement_product_demo.xml",
    ],
    "qweb": [
        "static/src/xml/replacement_template.xml",
    ],
    "installable": True,
}
