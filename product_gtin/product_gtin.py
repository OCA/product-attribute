# -*- coding: utf-8 -*-
##############################################################################
#
#    Product GTIN module for Odoo
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2011 Camptocamp (<http://www.camptocamp.at>)
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
import logging
_logger = logging.getLogger(__name__)

from openerp.osv import orm, fields

CONSTRAINT_MESSAGE = 'Error: Invalid EAN/GTIN code'
HELP_MESSAGE = ("EAN8 EAN13 UPC JPC GTIN \n"
                "http://en.wikipedia.org/wiki/Global_Trade_Item_Number")
                

# The official names of EANs, UPCs, etc. are now GTIN-x:
# GTIN-14 (was DUN-14, ITF)
# GTIN-13 (was EAN-13, CIP)
# GTIN-12 (was UCC-12, UPC)
# GTIN-8 (was EAN-8)
# From https://en.wikipedia.org/wiki/Global_Trade_Item_Number                


def check_gtinx(code):
    """
    The routine for calculating GTIN checksums is the same for all types,
    provided one starts at the end of the number (right-hand side) and works
    backwards.

    :param eancode: string, GTIN code
    :return: boolean    
    """
    total = 0
    gtin_len = len(code)
    for i in range(gtin_len-1):
        pos = int(gtin_len-2-i)
        if i % 2:
            total += int(code[pos])
        else:
            total += 3 * int(code[pos])
    check = 10 - (total % 10)
    check = check % 10

    return check == int(code[-1])    


VALID_GTIN_LENGTHS = [8, 12, 13, 14]


def check_gtin(eancode):
    if not eancode:
        return True
    if not len(eancode) in VALID_GTIN_LENGTHS:
        return False
    try:
        int(eancode)
    except:
        return False
    return check_gtinx(eancode)


class product_product(orm.Model):
    _inherit = "product.product"

    def _check_ean_key(self, cr, uid, ids):
        for rec in self.browse(cr, uid, ids):
            if not check_gtin(rec.ean13):
                return False
        return True

    _columns = {
        'ean13': fields.char(
            'EAN/GTIN', size=14,
            help="Code for %s" % HELP_MESSAGE),
    }

    _constraints = [(_check_ean_key, CONSTRAINT_MESSAGE, ['ean13'])]


class product_packaging(orm.Model):
    _inherit = "product.packaging"

    def _check_ean_key(self, cr, uid, ids):
        for rec in self.browse(cr, uid, ids):
            if not check_gtin(rec.ean):
                return False
        return True

    _columns = {
        'ean': fields.char(
            'EAN', size=14,
            help='Barcode number for %s' % HELP_MESSAGE),
        }

    _constraints = [(_check_ean_key, CONSTRAINT_MESSAGE, ['ean'])]


class res_partner(orm.Model):
    _inherit = "res.partner"

    def _check_ean_key(self, cr, uid, ids):
        for rec in self.browse(cr, uid, ids):
            if not check_gtin(rec.ean13):
                return False
        return True

    _columns = {
        'ean13': fields.char(
            'EAN', size=14,
            help="Code for %s" % HELP_MESSAGE),
        }

    _constraints = [(_check_ean_key, CONSTRAINT_MESSAGE, ['ean13'])]
    
    
if __name__ == '__main__':
    
    import unittest
    
    class TestEANCheckers(unittest.TestCase):
    
        def test_check_gtin(self):
            # Check all of the real-world GTINS via check_frin()

            # EAN13
            self.assertTrue(check_gtin('5013567421497'))
            
            # EAN8
            self.assertTrue(check_gtin('73513537'))  

            # UPC
            self.assertTrue(check_gtin('813922012941'))
            self.assertTrue(check_gtin('813922013030'))            
            
            # GTIN-14
            self.assertTrue(check_gtin('30012345678906'))
            
            # None should pass
            self.assertTrue(check_gtin(None))
            
            # Non-numeric string should fail
            self.assertFalse(check_gtin("ABCDEFG"))
            
            # Short numeric string should fail
            self.assertFalse(check_gtin("12345"))
            
            # GTINs with corrupted checksum should fail
            self.assertFalse(check_gtin('5013567421498'))            
            self.assertFalse(check_gtin('73513538'))            
            self.assertTrue(check_gtin('813922012941'))            
            self.assertFalse(check_gtin('813922013031'))            
            self.assertFalse(check_gtin('30012345678907'))                       


    unittest.main()
               
