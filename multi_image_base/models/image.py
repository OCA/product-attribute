# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#                  2015 Antiun Ingeniería <www.antiun.com>
#                       Jairo Llopis <yajo.sk8@gmail.com>
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


class ImageABC(models.AbstractModel):
    _name = "multi_image_base.image"
    _sql_constraints = [
        ('uniq_name_owner_id', 'UNIQUE(owner_id, name)',
         _('A document can have only one image with the same name.')),
    ]

    owner_id = fields.Many2one(
        comodel_name='multi_image_base.owner',  # Overwrite this in submodels
        string='Owner',
        required=True,
        ondelete='cascade')
    storage = fields.Selection(
        [('url', 'URL'), ('file', 'OS file'), ('db', 'Database')],
        default='db')
    name = fields.Char(
        'Image title',
        required=True,
        translate=True)
    filename = fields.Char()
    extension = fields.Char(
        'File extension',
        readonly=True)
    file_db_store = fields.Binary(
        'Image stored in database',
        filters='*.png,*.jpg,*.gif')
    path = fields.Char(
        "Image path",
        help="Image path")
    url = fields.Char(
        'Image remote URL')
    image_main = fields.Binary(
        "Full-sized image",
        compute="_get_image")
    image_medium = fields.Binary(
        "Medium-sized image",
        compute="_get_image_sizes",
        help="Medium-sized image. It is automatically resized as a 128 x "
             "128 px image, with aspect ratio preserved, only when the image "
             "exceeds one of those sizes. Use this field in form views or "
             "some kanban views.")
    image_small = fields.Binary(
        "Small-sized image",
        compute="_get_image_sizes",
        help="Small-sized image. It is automatically resized as a 64 x 64 px "
             "image, with aspect ratio preserved. Use this field anywhere a "
             "small image is required.")
    comments = fields.Text(
        'Comments',
        translate=True)

    @api.multi
    @api.depends('storage', 'path', 'file_db_store', 'url')
    def _get_image(self):
        """Get image data from the right storage type."""
        for s in self:
            s.image_main = getattr(s, "_get_image_from_%s" % s.storage)()

    @api.multi
    def _get_image_from_db(self):
        return self.file_db_store

    @api.multi
    def _get_image_from_file(self):
        if self.path and os.path.exists(self.path):
            try:
                with open(self.path, 'rb') as f:
                    return base64.b64encode(f.read())
            except Exception as e:
                _logger.error("Can not open the image %s, error : %s",
                              self.path, e, exc_info=True)
        else:
            _logger.error("The image %s doesn't exist ", self.path)

        return False

    @api.multi
    def _get_image_from_url(self):
        if self.url:
            try:
                (filename, header) = urllib.urlretrieve(self.url)
                with open(filename, 'rb') as f:
                    return base64.b64encode(f.read())
            except:
                _logger.error("URL %s cannot be fetched", self.url,
                              exc_info=True)

        return False

    @api.multi
    @api.depends('image_main')
    def _get_image_sizes(self):
        for s in self:
            try:
                vals = tools.image_get_resized_images(s.image_main)
            except:
                vals = {"image_medium": False,
                        "image_small": False}
            s.update(vals)

    @api.multi
    def _check_filestore(self):
        """check if the filestore is created, and do it otherwise."""
        for s in self:
            dir_path = os.path.dirname(s.path)
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            except OSError as e:
                raise exceptions.Warning(
                    _('The image filestore cannot be created, %s') % e)

    @api.model
    def _make_pretty(self, name):
        return name.replace('_', ' ').capitalize()

    @api.onchange('url')
    def _onchange_url(self):
        if self.url:
            filename = self.url.split('/')[-1]
            self.name, self.extension = os.path.splitext(filename)
            self.name = self._make_pretty(self.name)

    @api.onchange('path')
    def _onchange_path(self):
        if self.path:
            self.name, self.extension = os.path.splitext(os.path.basename(
                self.path))
            self.name = self._make_pretty(self.name)

    @api.onchange('filename')
    def _onchange_filename(self):
        if self.filename:
            self.name, self.extension = os.path.splitext(self.filename)
            self.name = self._make_pretty(self.name)

    @api.constrains('storage', 'url')
    def _check_url(self):
        if self.storage == 'url' and not self.url:
            raise exceptions.ValidationError(
                'You must provide an URL for the image.')

    @api.constrains('storage', 'path')
    def _check_path(self):
        if self.storage == 'file' and not self.path:
            raise exceptions.ValidationError(
                'You must provide a file path for the image.')

    @api.constrains('storage', 'file_db_store')
    def _check_store(self):
        if self.storage == 'db' and not self.file_db_store:
            raise exceptions.ValidationError(
                'You must provide an attached file for the image.')
