# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical = fields.Boolean(string="Is Medical", default=False)

    medical_certificate_url = fields.Char(string="CE Certificate medical devices")
    medical_class_id = fields.Many2one("medical.class", string="Medical Class")
    medicine_category_id = fields.Many2one(
        "medicine.category", string="Medical Category"
    )
    ppe_category_id = fields.Many2one("ppe.category", string="PPE Category")

    in_vitro_diagnostic = fields.Many2one(
        "in.vitro.diagnostic", string="In vitro diagnostics"
    )
    conformity_declaration = fields.Binary(
        string="Declaration of Conformity", attachment=True
    )
    doc_lot_related = fields.Boolean(string="Lot Related", default=False)
    doc_validity_date = fields.Date(string="Validity Date")
    ce_certificate_medical_class = fields.Binary(
        string="CE Certificate Medical class", attachment=True
    )
    ce_certificate_validity_date = fields.Date(string="Certificate Validity Date")
    notified_body_id = fields.Many2one(
        comodel_name="res.partner", ondelete="set null", string=u"Notified Body",
    )
