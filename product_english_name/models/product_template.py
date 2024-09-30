from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    english_name = fields.Char(compute="_compute_english_name")

    def _compute_english_name(self):
        lang = self.env.context.get("lang", "")
        english_us = self.env.ref("base.lang_en")
        for rec in self:
            if lang == "en_US":
                rec.english_name = ""
            else:
                rec.english_name = rec.with_context(lang=english_us.id).name
