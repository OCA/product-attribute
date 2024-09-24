from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductIdNumber(models.Model):
    _name = "product.product.id_number"
    _description = "Product Identification Number"

    name = fields.Char(string="ID Number", required=True)
    category_id = fields.Many2one(
        "product.product.id_category", string="Category", required=True
    )
    issued_by = fields.Many2one("res.partner")
    date_issued = fields.Date()
    expiry_date = fields.Date()
    place_of_issue = fields.Char(string="Place of Issue")
    product_id = fields.Many2one("product.product", string="Product")

    @api.constrains("date_issued", "expiry_date")
    def _check_check_date(self):
        for rec in self:
            if (
                rec.expiry_date
                and rec.date_issued
                and rec.date_issued > rec.expiry_date
            ):
                raise ValidationError(
                    _("Date of Issue cannot be greater than Date of Expiry")
                )

    @api.model
    def _cron_send_product_regi_expiry_notification(self):
        id_numbers = self.search([("expiry_date", "=", fields.Date.today())])
        email_template = self.env.ref(
            "product_identification.email_template_product_registration_expiry"
        )
        for record in id_numbers:
            context = {}
            receiver = (
                record.product_id.responsible_id
                or self.env.ref("stock.group_stock_manager").users[0]
            )
            context.update({"name": receiver.name})
            email_template.with_context(**context).send_mail(
                record.id,
                email_values={
                    "email_to": receiver.email,
                    "email_from": self.env.company.email,
                },
            )
