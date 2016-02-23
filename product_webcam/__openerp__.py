# -*- coding:utf-8 -*-
#
#
#    Copyright (C) 2016 Marçal Isern <marsal.isern@qubiq.es>.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    'name': 'Capture product picture with webcam',
    'version': '8.0.1.0.0',
    'category': 'Generic Modules/Product Attributes',
    'description': """
Product WebCam
===============

Capture product pictures with an attached web cam.
    """,
    'author': "Marçal Isern <info@qubiq.es>," "Michael Telahun Makonnen <mmakonnen@gmail.com>,"
    "Odoo Community Association (OCA)",
    'website': 'http://www.qubiq.es',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'web',
    ],
    'js': [
        'static/src/js/jquery.webcam.js',
        'static/src/js/product_webcam.js',
    ],
    'css': [
        'static/src/css/product_webcam.css',
    ],
    'qweb': [
        'static/src/xml/product_webcam.xml',
    ],
    'data': [
        #'product_webcam_data.xml',
        'product_webcam_view.xml',
    ],
    'installable': True,
    'active': False,
}
