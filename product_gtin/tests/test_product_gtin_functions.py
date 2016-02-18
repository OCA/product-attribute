# -*- coding: utf-8 -*-
# © 2015 Therp BV (<http://therp.nl>)
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common
from openerp.exceptions import ValidationError

VALID_EAN8_CODES = [
    # http://www.softmatic.com/barcode-ean-8.html
    "40123455",
    # http://www.barcodeisland.com/ean8.phtml
    "04210009",
]
VALID_EAN13_CODES = [
    # http://www.barcodeisland.com/ean13.phtml,
    "2000021262157",
]
VALID_UPC_CODES = [
    "012345678905",
    "080047440694",
    "123456789012",
]


class TestProductGtin(common.TransactionCase):

    def setUp(self):
        super(TestProductGtin, self).setUp()
        self.aean = self.env['abstract.ean']

    def test_is_pair(self):
        # http://en.wikipedia.org/wiki/Parity_of_zero
        self.assertTrue(self.aean._is_pair(0))

        # Testing random numbers.
        self.assertTrue(self.aean._is_pair(2), 'Should be True')
        self.assertTrue(self.aean._is_pair(4), 'Should be True')
        self.assertTrue(self.aean._is_pair(40), 'Should be True')

        self.assertFalse(self.aean._is_pair(1), 'Should be False')
        self.assertFalse(self.aean._is_pair(3), 'Should be False')
        self.assertFalse(self.aean._is_pair(5), 'Should be False')
        self.assertFalse(self.aean._is_pair(77), 'Should be False')

    # The codes have been tested against
    # http://www.hipaaspace.com/Medical_Data_Validation/Universal_Product_Code/
    # UPC_Validation.aspx noqa
    def test_upc_codes(self):
        for code in VALID_UPC_CODES:
            self.assertTrue(self.aean._check_upc(code))

    def test_returns_wrong_upc_codes(self):
        self.assertFalse(self.aean._check_upc(""))
        # test string
        self.assertFalse(self.aean._check_upc("odoo_oca"))
        # less than 12 numbers
        self.assertFalse(self.aean._check_upc("12345678901"))
        # 12 random numbers
        self.assertFalse(self.aean._check_upc("123456789013"))
        # more than 12 numbers
        self.assertFalse(self.aean._check_upc("12345678980123"))

    def test_ean8_codes(self):
        """Ean8 codes should not be valid for UPC."""
        for code in VALID_EAN8_CODES:
            self.assertFalse(self.aean._check_upc(code))

    def test_ean13_codes(self):
        """Ean13 codes should not be valid for UPC."""
        for code in VALID_EAN13_CODES:
            self.assertFalse(self.aean._check_upc(code))

    def test_returns_earn8_codes(self):
        for code in VALID_EAN8_CODES:
            self.assertTrue(self.aean._check_ean8(code))

    def test_returns_wrong_ean8_codes(self):
        self.assertFalse(self.aean._check_ean8(""))
        # test string
        self.assertFalse(self.aean._check_ean8("odoo_oca"))
        # less than 8 numbers
        self.assertFalse(self.aean._check_ean8("1234567"))
        # 8 random numbers
        self.assertFalse(self.aean._check_ean8("12345678"))
        self.assertFalse(self.aean._check_ean8("82766678"))
        # 9 numbers
        self.assertFalse(self.aean._check_ean8("123456789"))

    def test_return_ean8_codes(self):
        """Ean8 should not accept ean13"""
        for code in VALID_EAN13_CODES:
            self.assertFalse(self.aean._check_ean8(code))

    def test_return_upc_codes(self):
        """Ean8 should not accept UPC"""
        for code in VALID_UPC_CODES:
            self.assertFalse(self.aean._check_ean8(code))

    def test_return_ean13_codes(self):
        """test valid ean 13 number."""
        for code in VALID_EAN13_CODES:
            self.assertTrue(self.aean._check_ean13(code))

    def test_wrong_ean13_codes(self):
        self.assertFalse(self.aean._check_ean13(""))
        # test string
        self.assertFalse(self.aean._check_ean8("odoo_oca_sflx"))
        # less than 13 numbers
        self.assertFalse(self.aean._check_ean13("123456789012"))
        # 13 random numbers
        self.assertFalse(self.aean._check_ean13("1234567890123"))
        self.assertFalse(self.aean._check_ean13("1234514728123"))
        # 14 numbers
        self.assertFalse(self.aean._check_ean13("12345147281234"))

    def test_returns_ean8_codes(self):
        """Ean13 should not accept ean8"""
        for code in VALID_EAN8_CODES:
            self.assertFalse(self.aean._check_ean13(code))

    def test_returns_upc_codes(self):
        """Ean13 should not accept UPC"""
        for code in VALID_UPC_CODES:
            self.assertFalse(self.aean._check_ean13(code))

    def test_DICT_CHECK_EAN(self):
        """Check if the dict _DICT_CHECK_EAN exists."""
        self.assertTrue(self.aean._DICT_CHECK_EAN)

    def test_partner_barcode(self):
        partner = self.env['res.partner'].with_context(
            mail_create_nosubscribe=True)
        vals = {
            'name': 'test',
            'barcode': 't',
        }
        self.assertRaises(ValidationError, partner.create, vals)
        vals['barcode'] = "0075678164125"
        self.assertTrue(partner.create(vals))
