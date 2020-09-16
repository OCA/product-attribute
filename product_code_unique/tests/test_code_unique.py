# Copyright 2019 DynApps <https://www.dynapps.be/>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import psycopg2
from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestCodeUnique(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env['product.product']
        cls.product1 = cls.product_obj.create({
            'name': 'Test Product 1',
            'default_code': 'TSTP1',
        })

    def test_01_check_code_other(self):
        self.product2 = self.product_obj.create({
            'name': 'Test Product 2',
            'default_code': 'TSTP2',
        })

    def test_02_check_code_unique(self):
        with self.assertRaises(psycopg2.IntegrityError):
            with mute_logger('odoo.sql_db'), self.cr.savepoint():
                self.product2 = self.product_obj.create({
                    'name': 'Test Product 2',
                    'default_code': 'TSTP1',
                })

    def test_03_check_code_inactive(self):
        self.product2 = self.product_obj.create({
            'name': 'Test Product 2',
            'default_code': 'TSTP2',
        })
        self.product2.write({'active': False})
        self.product3 = self.product_obj.create({
            'name': 'Test Product 3',
            'default_code': 'TSTP2',
        })
        with self.assertRaises(psycopg2.IntegrityError):
            with mute_logger('odoo.sql_db'), self.cr.savepoint():
                self.product_obj.create({
                    'name': 'Test Product 4',
                    'default_code': 'TSTP2',
                })
