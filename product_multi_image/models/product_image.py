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
import base64
import urllib
import os
import logging
from openerp import models, fields, api, exceptions, _
from openerp import tools

_logger = logging.getLogger(__name__)


class ProductImage(models.Model):
    _name = "product.image"

    @api.one
    @api.depends('type', 'path', 'file_db_store', 'url')
    def _get_image(self):
        self.image = False
        if self.type == 'file':
            if self.path:
                if os.path.exists(self.path):
                    try:
                        with open(self.path, 'rb') as f:
                            self.image = base64.b64encode(f.read())
                    except Exception, e:
                        _logger.error("Can not open the image %s, error : %s",
                                      self.path, e, exc_info=True)
                else:
                    _logger.error("The image %s doesn't exist ", self.path)
        elif self.type == 'url':
            if self.url:
                try:
                    (filename, header) = urllib.urlretrieve(self.url)
                    with open(filename, 'rb') as f:
                        self.image = base64.b64encode(f.read())
                except:
                    _logger.error("URL %s cannot be fetched", self.url)
        elif self.type == 'db':
            self.image = self.file_db_store

    @api.one
    @api.depends('image')
    def _get_image_sizes(self):
        self.image_medium = False
        self.image_small = False
        if self.image:
            try:
                vals = tools.image_get_resized_images(
                    self.image, avoid_resize_medium=True)
                self.image_small = vals['image_small']
                self.image_medium = vals['image_medium']
            except:
                pass

    @api.multi
    def _check_filestore(self):
        """check if the filestore is created, and do it otherwise."""
        for product_image in self:
            dir_path = os.path.dirname(product_image.path)
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            except OSError, e:
                raise exceptions.Warning(
                    _('The image filestore can not be created, %s') % e)
        return True

    type = fields.Selection(
        selection=[('url', 'URL'), ('file', 'OS file'), ('db', 'DB')],
        default='db')
    name = fields.Char(string='Image title', required=True)
    extension = fields.Char(string='File extension')
    # Trick for displaying the extension and not to change it, but allowing
    # to save the real field (extension)
    extension2 = fields.Char(string='File extension', related="extension",
                             readonly=True)
    filename = fields.Char()
    file_db_store = fields.Binary(
        string='Image stored in database', filters='*.png,*.jpg,*.gif')
    path = fields.Char(string="Image path", help="Image path")
    url = fields.Char(string='Image remote URL')
    image = fields.Binary(
        compute="_get_image", string="File")
    image_medium = fields.Binary(
        compute="_get_image_sizes", string="Medium-sized image",
        help="Medium-sized image. It is automatically resized as a 128 x "
             "128 px image, with aspect ratio preserved, only when the image "
             "exceeds one of those sizes. Use this field in form views or "
             "some kanban views.")
    image_small = fields.Binary(
        compute="_get_image_sizes", string="Small-sized image",
        help="Small-sized image. It is automatically resized as a 64 x 64 px "
             "image, with aspect ratio preserved. Use this field anywhere a "
             "small image is required.")
    comments = fields.Text(string='Comments')
    product_id = fields.Many2one(
        comodel_name='product.template', string='Product', required=True,
        ondelete='cascade')

    def _make_pretty(self, name):
        return name.replace('_', ' ').capitalize()

    @api.onchange('url')
    def onchange_url(self):
        if self.url:
            filename = self.url.split('/')[-1]
            self.name, self.extension = os.path.splitext(filename)
            self.name = self._make_pretty(self.name)

    @api.onchange('path')
    def onchange_path(self):
        if self.path:
            self.name, self.extension = os.path.splitext(os.path.basename(
                self.path))
            self.name = self._make_pretty(self.name)

    @api.onchange('filename')
    def onchange_filename(self):
        if self.filename:
            self.name, self.extension = os.path.splitext(self.filename)
            self.name = self._make_pretty(self.name)

    @api.constrains('type', 'url')
    def _check_url(self):
        if self.type == 'url' and not self.url:
            raise exceptions.ValidationError(
                'You must provide a URL for the product image.')

    @api.constrains('type', 'path')
    def _check_path(self):
        if self.type == 'file' and not self.path:
            raise exceptions.ValidationError(
                'You must provide a file path for the product image.')

    @api.constrains('type', 'file_db_store')
    def _check_store(self):
        if self.type == 'db' and not self.file_db_store:
            raise exceptions.ValidationError(
                'You must provide an attached file for the product image.')

    _sql_constraints = [
        ('uniq_name_product_id', 'UNIQUE(product_id, name)',
         _('A product can have only one image with the same name')),
    ]
