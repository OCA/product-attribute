# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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


def migrate(cr, version):
    """get our value from product_product"""
    cr.execute(
        'update product_template t set '
        'manufacturer = coalesce(t.manufacturer, p.manufacturer), '
        'manufacturer_pname = '
        'coalesce(t.manufacturer_pname, p.manufacturer_pname), '
        'manufacturer_pref = '
        'coalesce(t.manufacturer_pref, p.manufacturer_pref) '
        'from product_product p where p.product_tmpl_id=t.id')
