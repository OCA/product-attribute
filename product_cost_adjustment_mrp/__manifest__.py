# Copyright 2021 - Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Cost Adjustment MRP",
    "summary": "Adds impacted MO's to cost adjustments.",
    "version": "14.0.1.0.0",
    "development_status": "Production/Stable",
    "maintainers": ["patrickrwilson"],
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product_cost_adjustment", "mrp"],
    "data": [
        "views/cost_adjustment_line.xml",
        "report/report_mrp.xml",
    ],
}
