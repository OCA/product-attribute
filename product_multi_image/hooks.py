# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

_logger = logging.getLogger(__name__)


try:
    from odoo.addons.base_multi_image.hooks import (
        post_init_hook_for_submodules,
        uninstall_hook_for_submodules,
    )
except ImportError:
    _logger.info("Cannot import base_multi_image hooks")


def post_init_hook(env):
    post_init_hook_for_submodules(env, "product.template", "image_1920")
    post_init_hook_for_submodules(env, "product.product", "image_variant_1920")


def uninstall_hook(env):
    """Remove multi images for models that no longer use them."""
    uninstall_hook_for_submodules(env, "product.template")
    uninstall_hook_for_submodules(env, "product.product")
