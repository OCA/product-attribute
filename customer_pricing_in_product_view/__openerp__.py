# -*- coding: utf-8 -*-
# © 2014 O4SB <http://o4sb.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Display Customer Price in Product View',
    'version': '8.0.1.2.1',
    'category': 'Sales',
    'author': "O4SB - Graeme Gellatly,Odoo Community Association (OCA)",
    'website': 'http://www.o4sb.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
