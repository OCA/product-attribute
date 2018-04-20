##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from openerp import models, api, fields, _
from odoo.exceptions import ValidationError


class ProductAdrClass(models.Model):
    _name = 'product.adr.class'

    un_number = fields.Char(string='UN Number', size=4, required=True)
    name = fields.Char(string='Name', size=64, required=True)
    picking_text = fields.Text(string='Description text in stock picking',
                               size=256, translate=True)

    @api.constrains('un_number')
    def _check_un_number(self):
        error_msg = _("UN Number should be a number between 0001 and 3600.")
        if self.un_number:
            if self.un_number.isdigit():
                if int(self.un_number) < 0 or \
                   int(self.un_number) > 3600:
                    raise ValidationError(error_msg)
            else:
                raise ValidationError(error_msg)

    @api.multi
    def name_get(self):
        return [(record.id, "[%s] %s" % (record.un_number, record.name)) for
                record in self]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain_name = ['|', ('name', 'ilike', name),
                       ('un_number', 'ilike', name)]
        recs = self.search(domain_name + args, limit=limit)
        return recs.name_get()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    adr_class_id = fields.Many2one('product.adr.class',
                                   string='Product ADR Class')
