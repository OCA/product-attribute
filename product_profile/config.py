# coding: utf-8
##############################################################################
#
#    Author: David BEAL
#    Copyright 2015 Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields
from .product import PROFILE_MENU


class BaseConfigSettings(models.Model):
    _inherit = 'base.config.settings'

    group_product_profile = fields.Boolean(
        string="Display Profile fields",
        implied_group='product_profile.group_product_profile',
        help="Display fields computed by product profile "
             "module.\nFor debugging purpose"
             "\nsee menu %s" % PROFILE_MENU)
