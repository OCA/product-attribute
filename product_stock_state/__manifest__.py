# Copyright 2017 Akretion (http://www.akretion.com).
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Product Stock State",
    "summary": "Compute the state of a product's stock"
    "the stock level and sale_ok field",
    "version": "13.0.1.0.0",
    "website": "https://github.com/oca/product-attribute",
    "author": " Akretion, GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_stock"],
    "data": [
        "security/res_groups.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/product_category_view.xml",
        "views/res_config_settings_view.xml",
        "views/res_company_view.xml",
        "data/data.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_category.xml",
        "demo/product_product.xml",
        "demo/product_category.xml",
    ],
    "qweb": [],
    "maintainers": ["sebastienbeau", "legalsylvain", "kevinkhao"],
}
