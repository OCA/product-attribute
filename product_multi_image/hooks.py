# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.multi_image_base.hooks import post_init_hook_for_submodules


def post_init_hook(cr, registry):
    post_init_hook_for_submodules(cr, registry, "product.template", "image")
