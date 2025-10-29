# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductScaleSystem(models.Model):
    _name = "product.scale.system"
    _description = "Product Scale System"

    # Constant section
    _ENCODING_SELECTION = [
        ("iso-8859-1", "Latin 1 (iso-8859-1)"),
        ("cp1252", "Latin 1 (cp1252)"),
        ("utf-8", "UTF-8"),
    ]

    # Column Section
    name = fields.Char(required=True)
    company_id = fields.Many2one(
        "res.company",
        index=True,
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    ftp_host = fields.Char(string="FTP Server Host", default="xxx.xxx.xxx.xxx")
    ftp_port = fields.Integer("FTP Server Port", default=21)
    ftp_login = fields.Char()
    ftp_password = fields.Char()
    encoding = fields.Selection(
        _ENCODING_SELECTION,
        required=True,
        default="iso-8859-1",
    )
    csv_relative_path = fields.Char(required=True, default="/")
    product_image_relative_path = fields.Char(required=True, default="/")
    product_text_file_pattern = fields.Char(
        required=True,
        help="Pattern "
        "of the Product file. Use % to include dated information.\n"
        " Ref: https://docs.python.org/2/library/time.html#time.strftime",
        default="product.csv",
    )
    external_text_file_pattern = fields.Char(
        required=True,
        help="Pattern"
        " of the External Text file. Use % to include dated information.\n"
        " Ref: https://docs.python.org/2/library/time.html#time.strftime",
        default="external_text.csv",
    )
    product_line_ids = fields.One2many(
        "product.scale.system.product.line",
        "scale_system_id",
    )
    field_ids = fields.Many2many(
        "ir.model.fields",
        compute="_compute_field_ids",
        readonly=True,
        store=True,
    )
    send_images = fields.Boolean("Send Image To Scale", default=False)

    @api.depends("product_line_ids")
    def _compute_field_ids(self):
        for rec in self:
            field_ids = rec.field_ids.ids or []
            for line in rec.product_line_ids:
                if line.field_id and line.field_id not in rec.field_ids:
                    field_ids.append(line.field_id.id)
            rec.field_ids = [(6, 0, field_ids)]

    def test_button(self):
        for rec in self:
            ftp_ret = self.env["product.scale.log"].ftp_connection_open(
                rec, raise_error=True
            )
            self.env["product.scale.log"].ftp_connection_close(ftp_ret)
