# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class Owner(models.AbstractModel):
    _name = "multi_image_base.owner"

    image_ids = fields.One2many(
        comodel_name='multi_image_base.image',  # Overwrite this in submodels
        inverse_name='owner_id',
        string='Images',
        copy=True)
    image_main = fields.Binary(
        string="Main image",
        compute="_get_main_image",
        store=False,
        inverse="_set_main_image")
    image_medium = fields.Binary(
        string="Medium image",
        compute="_get_main_image",
        inverse="_set_main_image_medium",
        store=False)
    image_small = fields.Binary(
        string="Small image",
        compute="_get_main_image",
        inverse="_set_main_image_small",
        store=False)

    @api.multi
    def _inverse_image_main(self):
        """Save images."""

    @api.one
    @api.depends('image_ids')
    def _get_main_image(self):
        self.image_main = False
        self.image_medium = False
        self.image_small = False
        if self.image_ids:
            self.image_main = self.image_ids[0].image_main
            self.image_medium = self.image_ids[0].image_medium
            self.image_small = self.image_ids[0].image_small

    @api.multi
    def _set_image(self, image):
        if self.image:
            if self.image_ids:
                self.image_ids[0].write({'storage': 'db',
                                         'file_db_store': image})
            else:
                self.image_ids = [(0, 0, {'storage': 'db',
                                          'file_db_store': image,
                                          'name': _('Main image')})]
        elif self.image_ids:
            self.image_ids[0].unlink()

    @api.one
    def _set_main_image(self):
        self._set_image(self.image_main)

    @api.one
    def _set_main_image_medium(self):
        self._set_image(self.image_medium)

    @api.one
    def _set_main_image_small(self):
        self._set_image(self.image_small)

    @api.multi
    def write(self, vals):
        if 'image_medium' in vals and 'image_ids' in vals:
            # Inhibit the write of the image when images tab has been touched
            del vals['image_medium']
        return super(Owner, self).write(vals)
