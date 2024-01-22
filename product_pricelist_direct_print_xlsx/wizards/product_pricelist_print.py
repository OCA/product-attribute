# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductPricelistPrint(models.TransientModel):
    _inherit = "product.pricelist.print"

    breakage_per_category = fields.Boolean(default=True)

    show_internal_category = fields.Boolean(string="Show internal categories")

    def export_xlsx(self):
        self.ensure_one()
        return self.env.ref("product_pricelist_direct_print_xlsx.report").report_action(
            self
        )
