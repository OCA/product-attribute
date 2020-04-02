# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductScaleSystem(models.Model):
    _name = 'product.scale.system'
    _description = 'Product Scale System'

    # Constant section
    _ENCODING_SELECTION = [
        ('iso-8859-1', 'Latin 1 (iso-8859-1)'),
        ('cp1252', 'Latin 1 (cp1252)'),
        ('utf-8', 'UTF-8'),
    ]

    # Compute Section
    @api.depends('product_line_ids')
    def _get_field_ids(self):
        for system in self:
            for product_line in system.product_line_ids:
                if product_line.field_id:
                    product_line.field_id.product_system_scale_id = system.id

    # Column Section
    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        index=True,
        default=lambda self:
        self.env['res.company']._company_default_get('product.template')
    )
    active = fields.Boolean(string='Active', default=True)
    ftp_host = fields.Char(
        string='FTP Server Host',
        oldname='ftp_url',
        default='xxx.xxx.xxx.xxx'
    )
    ftp_port = fields.Integer(
        'FTP Server Port',
        default=21
    )
    ftp_login = fields.Char('FTP Login')
    ftp_password = fields.Char('FTP Password')
    encoding = fields.Selection(
        _ENCODING_SELECTION,
        string='Encoding',
        required=True,
        default='iso-8859-1'
    )
    csv_relative_path = fields.Char(
        'Relative Path for CSV',
        required=True, default='/'
    )
    product_image_relative_path = fields.Char(
        'Relative Path for Product Images',
        required=True, default='/'
    )
    product_text_file_pattern = fields.Char(
        'Product Text File Pattern',
        required=True,
        help="Pattern "
        "of the Product file. Use % to include dated information.\n"
        " Ref: https://docs.python.org/2/library/time.html#time.strftime",
        default='product.csv'
    )
    external_text_file_pattern = fields.Char(
        'External Text File Pattern',
        required=True,
        help="Pattern"
        " of the External Text file. Use % to include dated information.\n"
        " Ref: https://docs.python.org/2/library/time.html#time.strftime",
        default='external_text.csv'
    )
    product_line_ids = fields.One2many(
        'product.scale.system.product.line',
        'scale_system_id',
        'Product Lines'
    )
    field_ids = fields.Many2many('ir.model.fields', string='Fields')
    send_images = fields.Boolean(
        'Send Image To Scale',
        default=False
    )

    @api.onchange('product_line_ids')
    def onchange_product_line_ids(self):
        for line in self.product_line_ids:
            if line.field_id and line.field_id not in self.field_ids:
                ids = self.field_ids.ids
                ids.append(line.field_id.id)
                self.field_ids = [(6, 0, ids)]
