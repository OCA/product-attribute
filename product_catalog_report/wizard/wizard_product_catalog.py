# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>)
# Copyright (C) 2020 ForgeFlow S.L. (<http://www.forgeflow.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WizardProductCatalog(models.TransientModel):
    _name = "res.partner.product_catalog"
    _description = "Wizard Product Catalog"

    def _get_language(self):
        lang_obj = self.env["res.lang"]
        languages = lang_obj.search([("active", "=", True)])
        return [(lang.code, lang.name) for lang in languages]

    def _get_default_report_lang(self):
        partner_obj = self.env["res.partner"]
        partners = partner_obj.browse(self.env.context.get("active_ids", []))
        return partners[0].lang

    report_lang = fields.Selection(
        selection=_get_language, string="Language", default=_get_default_report_lang
    )
    categories = fields.Many2many(
        comodel_name="product.category", string="Select Category", required=True
    )

    def create_product_catalog(self):
        self.ensure_one()
        data = {}
        data["ids"] = self.env.context.get("active_ids", [])
        data["model"] = "res.partner"
        data["form"] = self.read(["report_lang", "categories"])[0]
        return self.env.ref(
            "product_catalog_report.action_report_product_catalog"
        ).report_action(self, data=data)
