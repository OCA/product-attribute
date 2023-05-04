# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Weight from bom Calculation",
    "version": "16.0.1.0.0",
    "author": "Savoir-faire Linux,Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Warehouse",
    "summary": "Allows to calculate products weight from its components.",
    "depends": [
        "product_weight_from_bom",
        "queue_job",
    ],
    "data": [
        "data/queue_job_channel_data.xml",
        "data/queue_job_function_data.xml",
    ],
    "installable": True,
}
