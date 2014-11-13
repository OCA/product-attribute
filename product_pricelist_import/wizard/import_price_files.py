# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import fields, models, api, exceptions, _
import base64
import cStringIO
import tempfile
import csv


class ImportPriceFile(models.TransientModel):
    _name = 'import.price.file'
    _description = 'Import Price List File'

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename', required=False)
    delimeter = fields.Char('Delimeter', default=',',
                            help='Default delimeter is ","')
    file_type = fields.Selection([('csv', 'CSV'), ('xls', 'XLS')], 'File Type',
                                 required=True, default='csv')

    def _import_csv(self, load_id, file_data, delimeter=';'):
        """ Imports data from a CSV file in defined object.
        @param load_id: Loading id
        @param file_data: Input data to load
        @param delimeter: CSV file data delimeter
        @return: Imported file number
        """
        file_line_obj = self.env['product.pricelist.load.line']
        data = base64.b64decode(file_data)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        reader = csv.reader(file_input, delimiter=str(delimeter),
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        # keys2 = reader_info[0]
        counter = 0
        keys = ['code', 'info', 'price', 'discount_1', 'discount_2',
                'retail', 'pdv1', 'pdv2']
        if not isinstance(keys, list):
            raise exceptions.Warning(_("Not a valid file!"))
        del reader_info[0]
        for i in range(len(reader_info)):
            field = reader_info[i]
            values = dict(zip(keys, field))
            file_line_obj.create(
                {'code': values['code'], 'info': values['info'],
                 'price': values['price'].replace(',', '.'),
                 'discount_1': float(values['discount_1'].replace(',', '.')),
                 'discount_2': float(values['discount_2'].replace(',', '.')),
                 'retail': float(values['retail'].replace(',', '.')),
                 'pdv1': float(values['pdv1'].replace(',', '.')),
                 'pdv2': float(values['pdv2'].replace(',', '.')),
                 'fail': True, 'fail_reason': _('No Processed'),
                 'file_load': load_id
                 })
            counter += 1
        return counter

    def _import_xls(self, load_id, file_data):
        """ Imports data from a XLS file in defined object.
        @param load_id: Loading id
        @param file_data: Input data to load
        @return: Imported file number
        """
        try:
            import xlrd
        except ImportError:
            exceptions.Warning(_("xlrd python lib  not installed"))
        file_line_obj = self.env['product.pricelist.load.line']
        file_1 = base64.decodestring(file_data)
        (fileno, fp_name) = tempfile.mkstemp('.xls', 'openerp_')
        openfile = open(fp_name, "w")
        openfile.write(file_1)
        book = xlrd.open_workbook(fp_name)
        sheet = book.sheet_by_index(0)
        values = {}
        keys = ['code', 'info', 'price', 'discount_1',
                'discount_2', 'retail', 'pdv1', 'pdv2']
        # keys2 = sheet.row_values(0,0, end_colx=sheet.ncols)
        for counter in range(sheet.nrows - 1):
            # grab the current row
            rowValues = sheet.row_values(counter + 1, 0,
                                         end_colx=sheet.ncols)
            row = map(lambda x: str(x), rowValues)
            values = dict(zip(keys, row))
            file_line_obj.create(
                {'code': values['code'], 'info': values['info'],
                 'price': values['price'].replace(',', '.'),
                 'discount_1': float(values['discount_1'].replace(',', '.')),
                 'discount_2': float(values['discount_2'].replace(',', '.')),
                 'retail': float(values['retail'].replace(',', '.')),
                 'pdv1': float(values['pdv1'].replace(',', '.')),
                 'pdv2': float(values['pdv2'].replace(',', '.')),
                 'fail': True, 'fail_reason': _('No Processed'),
                 'file_load': load_id
                 })
            counter += 1
        return counter

    @api.multi
    def action_import(self):
        file_load_obj = self.env['product.pricelist.load']
        context = self._context
        if 'active_id' in context:
            load_id = context['active_id']
            file_load = file_load_obj.browse(load_id)
        for line in file_load.file_lines:
            line.unlink()
        for wiz in self:
            if not wiz.data:
                raise exceptions.Warning(_("You need to select a file!"))
            date_hour = fields.datetime.now()
            actual_date = fields.date.today()
            filename = wiz.name
            if wiz.file_type == 'csv':
                counter = self._import_csv(load_id, wiz.data, wiz.delimeter)
            elif wiz.file_type == 'xls':
                counter = self._import_xls(load_id, wiz.data)
            else:
                raise exceptions.Warning(_("Not a .csv/.xls file found"))
            file_load.write({'name': ('%s_%s') % (filename, actual_date),
                             'date': date_hour, 'fails': counter,
                             'file_name': filename, 'process': counter})
        return counter
