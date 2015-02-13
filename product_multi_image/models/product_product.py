# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.template"

    @api.one
    @api.depends('image_ids')
    def _get_main_image(self):
        self.product_image = False
        self.image_medium = False
        self.image_small = False
        if self.image_ids:
            self.product_image = self.image_ids[0].image
            self.image_medium = self.image_ids[0].image_medium
            self.image_small = self.image_ids[0].image_small

    def _set_image(self, image):
        if self.image:
            if self.image_ids:
                self.image_ids[0].write({'type': 'db',
                                         'file_db_store': image})
            else:
                self.image_ids = [(0, 0, {'type': 'db',
                                          'file_db_store': image,
                                          'name': _('Main image')})]
        elif self.image_ids:
            self.image_ids[0].unlink()

    @api.one
    def _set_main_image(self):
        self._set_image(self.product_image)

    @api.one
    def _set_main_image_medium(self):
        self._set_image(self.image_medium)

    @api.one
    def _set_main_image_small(self):
        self._set_image(self.image_small)

    image_ids = fields.One2many(
        comodel_name='product.image', inverse_name='product_id',
        string='Product images', copy=True)
    product_image = fields.Binary(
        string="Main image", compute="_get_main_image", store=False,
        inverse="_set_main_image")
    image_medium = fields.Binary(
        compute="_get_main_image", inverse="_set_main_image_medium",
        store=False)
    image_small = fields.Binary(
        compute="_get_main_image", inverse="_set_main_image_small",
        store=False)

    @api.multi
    def write(self, vals):
        if 'image_medium' in vals and 'image_ids' in vals:
            # Inhibit the write of the image when images tab has been touched
            del vals['image_medium']
        return super(ProductProduct, self).write(vals)
