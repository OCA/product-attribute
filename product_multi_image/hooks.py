# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

try:
    from openerp.addons.base_multi_image.hooks import (
        pre_init_hook_for_submodules)
except ImportError:
    # Don't complain, as this will be solved as dependency when needed
    pass


def pre_init_hook(cr):
    pre_init_hook_for_submodules(cr, "product.template", "image")
