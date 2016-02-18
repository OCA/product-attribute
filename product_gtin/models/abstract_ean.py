# -*- coding: utf-8 -*-
# © 2004-2011 Tiny SPRL (<http://tiny.be>)
# © 2010-2011 Camptocamp Austria (<http://www.camptocamp.at>)
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models
from openerp.tools.translate import _
from openerp.exceptions import ValidationError
import operator
import logging
_logger = logging.getLogger(__name__)


class AbstractEan(models.AbstractModel):
    _name = 'abstract.ean'
    _description = 'Abstract Ean'

    @api.model
    def _is_pair(self, x):
        return not x % 2

    @api.model
    def _check_ean8(self, eancode):
        """Check if the given ean code answer ean8 requirements
        For more details: http://en.wikipedia.org/wiki/EAN-8
        :param eancode: string, ean-8 code
        :return: boolean
        """
        if not eancode or not eancode.isdigit():
            return False
        if not len(eancode) == 8:
            _logger.warn('Ean8 code has to have a length of 8 characters.')
            return False
        sum = 0
        ean_len = int(len(eancode))
        for i in range(ean_len - 1):
            if self._is_pair(i):
                sum += 3 * int(eancode[i])
            else:
                sum += int(eancode[i])
        check = 10 - operator.mod(sum, 10)
        if check == 10:
            check = 0
        return check == int(eancode[-1])

    @api.model
    def _check_upc(self, upccode):
        """Check if the given code answers upc requirements
        For more details:
        http://en.wikipedia.org/wiki/Universal_Product_Code

        :param upccode: string, upc code
        :return: bool
        """
        if not upccode or not upccode.isdigit():
            return False
        if not len(upccode) == 12:
            _logger.warn('UPC code has to have a length of 12 characters.')
            return False
        sum_pair = 0
        ean_len = int(len(upccode))
        for i in range(ean_len - 1):
            if self._is_pair(i):
                sum_pair += int(upccode[i])
        sum = sum_pair * 3
        for i in range(ean_len - 1):
            if not self._is_pair(i):
                sum += int(upccode[i])
        check = ((sum / 10 + 1) * 10) - sum
        return check == int(upccode[-1])

    @api.model
    def _check_ean13(self, eancode):
        """Check if the given ean code answer ean13 requirements
        For more details:
        http://en.wikipedia.org/wiki/International_Article_Number_%28EAN%29
        :param eancode: string, ean-13 code
        :return: boolean
        """
        if not eancode or not eancode.isdigit():
            return False
        if not len(eancode) == 13:
            _logger.warn('Ean13 code has to have a length of 13 characters.')
            return False
        sum = 0
        ean_len = int(len(eancode))
        for i in range(ean_len - 1):
            pos = int(ean_len - 2 - i)
            if self._is_pair(i):
                sum += 3 * int(eancode[pos])
            else:
                sum += int(eancode[pos])
        check = 10 - operator.mod(sum, 10)
        if check == 10:
            check = 0
        return check == int(eancode[-1])

    @api.model
    def _check_ean11(self, eancode):
        pass

    @api.model
    def _check_gtin14(self, eancode):
        pass

    _DICT_CHECK_EAN = {
        8: _check_ean8,
        11: _check_ean11,
        12: _check_upc,
        13: _check_ean13,
        14: _check_gtin14,
    }

    @api.model
    def _check_code(self, barcode):
        nb_digit = len(barcode)
        if nb_digit not in self._DICT_CHECK_EAN:
            raise ValidationError(_('Size of EAN/GTIN code is not valid'))
        try:
            int(barcode)
        except:
            raise ValidationError(_('EAN/GTIN Should be a digit'))
        if not self._DICT_CHECK_EAN[nb_digit](self, barcode):
            raise ValidationError(
                _('EAN/GTIN format is not a valid format'))
