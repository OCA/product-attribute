# Copyright (C) 2021-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import odoo.addons.decimal_precision as dp


class WizardPreviewPricelistMarginLine(models.TransientModel):
    _name = "wizard.preview.pricelist.margin.line"
    _description = "Wizard - Preview Pricelist Margin Line"

    wizard_id = fields.Many2one(
        comodel_name="wizard.preview.pricelist.margin", string="Wizard",
        ondelete="cascade", readonly=True)

    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist", string="Pricelist",
        ondelete="cascade", readonly=True)

    currency_id = fields.Many2one(
        comodel_name="res.currency", string="Currency",
        related="pricelist_id.currency_id", readonly=True,
        ondelete="cascade")

    price_vat_excl = fields.Float(
        string="Unit Sales Price (Excl.)",
        readonly=True
    )
    price_vat_incl = fields.Float(
        string="Unit Sales Price (Incl.)",
        readonly=True
    )

    margin = fields.Float(
        string='Margin',
        store=True,
        digits=dp.get_precision('Product Price'), readonly=True,
    )

    margin_percent = fields.Float(
        string='Margin (%)',
        store=True,
        digits=dp.get_precision('Product Price'), readonly=True,
    )

    bg_color = fields.Char(compute="_compute_bg_color")

    def _compute_bg_color(self):
        for line in self:
            if line.margin_percent < 0:
                line.bg_color = "#FF3333"
            else:
                line.bg_color = "rgb(105, {green:.0f}, {blue:.0f})".format(
                    green=105 + 1.5 * line.margin_percent,
                    blue=255 - 1.5 * line.margin_percent)
