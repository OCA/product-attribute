# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]

    # image, image_medium, image_small fields are not available since 13.0
