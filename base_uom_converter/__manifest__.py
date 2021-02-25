# Copyright <2021> <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base UoM converter",
    "summary": "Convert quantities from an UoM category to an other one.",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "category": "Sales/Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Pierre Verkest, Odoo Community Association (OCA)",
    "installable": True,
    "depends": [
        "uom",
        # Currently this module depends on sale module to:
        # * place menu at the right place close to uom configurations
        # * let sales manager to manage scales converter (as sale depends on
        #   sales_team)
        "sale",
    ],
    "data": [
        "views/uom-converter.xml",
        "views/menu.xml",
        "security/ir.model.access.csv",
    ],
}
