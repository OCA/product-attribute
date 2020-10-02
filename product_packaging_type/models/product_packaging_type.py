# -*- coding: utf-8 -*-
# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackagingType(models.Model):
    _name = "product.packaging.type"
    _description = "Type management for product.packaging"
    _order = "sequence, code"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    active = fields.Boolean(default=True)
    is_default = fields.Boolean()

    @api.constrains("is_default")
    def _check_is_default(self):
        msg = False
        default_count = self.search_count([("is_default", "=", True)])
        if default_count == 0:
            msg = _('There must be one product packaging type set as "Is Default".')
        elif default_count > 1:
            msg = _('Only one product packaging type can be set as "Is Default".')
        if msg:
            raise ValidationError(msg)

    @api.depends("name", "code")
    def _compute_display_name(self):
        return super(ProductPackagingType, self)._compute_display_name()

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, u"{} ({})".format(record.name, record.code)))
        return result
