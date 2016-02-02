# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "multi_image_base.owner"]

    image = fields.Binary(related="image_main", store=False)
    image_medium = fields.Binary(related="image_main_medium", store=False)
    image_small = fields.Binary(related="image_main_small", store=False)

    @api.multi
    def _set_image(self, name, value, args):
        return self._set_multi_image_main(value, name)
