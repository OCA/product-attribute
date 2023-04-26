# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

try:
    from odoo.addons.base_multi_image.hooks import (
        pre_init_hook_for_submodules,
        uninstall_hook_for_submodules,
    )
except ImportError:
    pass


def pre_init_hook(cr):
    pre_init_hook_for_submodules(cr, "product.template", "image_1920")
    pre_init_hook_for_submodules(cr, "product.product", "image_variant_1920")


def uninstall_hook(cr, registry):
    """Remove multi images for models that no longer use them."""
    uninstall_hook_for_submodules(cr, registry, "product.template")
    uninstall_hook_for_submodules(cr, registry, "product.product")
