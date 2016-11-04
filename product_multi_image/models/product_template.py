# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]

    image = fields.Binary(
        related='image_main',
        store=False,
    )
    image_medium = fields.Binary(
        related='image_main_medium',
        store=False,
    )
    image_small = fields.Binary(
        related='image_main_small',
        store=False,
    )
