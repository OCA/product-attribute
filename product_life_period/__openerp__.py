# -*- coding: utf-8 -*-
# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product life period",
    "version": "8.0.1.0.0",
    'author': "Acsone SA/NV, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "http://www.acsone.eu",
    "depends": ["product",
                ],
    "data": ["views/product_life_period_views.xml",
             "security/ir.model.access.csv",
             ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
