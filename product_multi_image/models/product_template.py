# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class ProductTemplate(orm.Model):
    """Reference core image fields to multi-image variants.

    It is needed to use v7 api here because core model fields use the ``multi``
    attribute, that has no equivalent in v8, and it needs to be disabled or
    bad things will happen. For more reference, see
    https://github.com/odoo/odoo/issues/10799
    """
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]
    _columns = {
        "image": fields.related(
            "image_main",
            type="binary",
            store=False,
            multi=False),
        "image_medium": fields.related(
            "image_main_medium",
            type="binary",
            store=False,
            multi=False),
        "image_small": fields.related(
            "image_main_small",
            type="binary",
            store=False,
            multi=False)
    }
