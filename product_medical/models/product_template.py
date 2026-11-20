# Copyright 2020 Iryna Vyshnevska,Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical = fields.Boolean(default=False)

    medical_certificate_url = fields.Char(string="CE Certificate medical devices")
    medical_class_id = fields.Many2one("medical.class", string="Medical Device Class")
    medicine_category_id = fields.Many2one("medicine.category", string="Drug Category")
    medical_ppe_category_id = fields.Many2one("ppe.category", string="PPE Category")

    medical_in_vitro_diagnostic = fields.Many2one(
        "in.vitro.diagnostic", string="In vitro diagnostics"
    )
    medical_conformity_declaration_ids = fields.Many2many(
        "ir.attachment",
        relation="product_medical_conformity_declaration_rel",
        column1="product_template_id",
        column2="attachment_id",
        string="Declaration of Conformity",
    )
    medical_doc_lot_related = fields.Boolean(string="Lot Related", default=False)
    medical_doc_validity_date = fields.Date(string="Validity Date")
    medical_ce_certificate_class_ids = fields.Many2many(
        "ir.attachment",
        relation="product_medical_ce_certificate_class_rel",
        column1="product_template_id",
        column2="attachment_id",
        string="CE Certificate",
    )
    medical_ce_certificate_validity_date = fields.Date(
        string="Certificate Validity Date"
    )
    medical_notified_body_id = fields.Many2one(
        comodel_name="res.partner",
        ondelete="set null",
        string="Notified Body",
    )
