# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, tools


class Owner(models.AbstractModel):
    _name = "multi_image_base.owner"

    image_ids = fields.One2many(
        comodel_name='multi_image_base.image',
        inverse_name='owner_id',
        string='Images',
        domain=lambda self: [("owner_model", "=", self._name)],
        copy=True)
    image_main = fields.Binary(
        string="Main image",
        store=False,
        compute="_get_multi_image_main",
        inverse="_set_multi_image_main")
    image_medium = fields.Binary(
        string="Medium image",
        compute="_get_multi_image_main",
        inverse="_set_multi_image_main",
        store=False)
    image_small = fields.Binary(
        string="Small image",
        compute="_get_multi_image_main",
        inverse="_set_multi_image_main",
        store=False)

    @api.multi
    @api.depends('image_ids')
    def _get_multi_image_main(self):
        """Get a the main image for this object.

        This is provided as a compatibility layer for submodels that already
        had one image per record.
        """
        for s in self:
            s.image_main = False
            s.image_medium = False
            s.image_small = False
            if s.image_ids:
                s.image_main = s.image_ids[0].image_main
                s.image_medium = s.image_ids[0].image_medium
                s.image_small = s.image_ids[0].image_small

    @api.multi
    def _set_multi_image_main(self, image=False, name=None):
        """Save or delete the main image for this record.

        This is provided as a compatibility layer for submodels that already
        had one image per record.
        """
        # Values to save
        values = {
            "storage": "db",
            "file_db_store": tools.image_resize_image_big(image),
            "owner_model": self._name,
        }
        if name:
            values["name"] = name

        for s in self:
            if image:
                import wdb; wdb.set_trace()  # TODO DELETE
                values["owner_id"] = s.id
                # Editing
                if s.image_ids:
                    values.setdefault("name", name or _("Main image"))
                    s.image_ids[0].write(values)
                # Adding
                else:
                    s.image_ids = [(0, 0, values)]
            # Deleting
            elif s.image_ids:
                s.image_ids[0].unlink()

    @api.multi
    def write(self, vals):
        if 'image_medium' in vals and 'image_ids' in vals:
            # Inhibit the write of the image when images tab has been touched
            del vals['image_medium']
        return super(Owner, self).write(vals)

    @api.multi
    def unlink(self):
        """Mimic `ondelete="cascade"` for multi images."""
        images = self.mapped("image_ids")
        result = super(Owner, self).unlink()
        if result:
            images.unlink()
        return result
