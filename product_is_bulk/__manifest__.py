# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Is Bulk",
    "summary": "Compute or Set Product as Bulk",
    "version": "16.0.2.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Grap",
    "maintainers": ["quentinDupont"],
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product_compute_template_field_from_variant_helper",
        "product_uom_measure_type",
    ],
    "data": [
        "views/view_product_product.xml",
        "views/view_product_template.xml",
    ],
    "installable": True,
}
