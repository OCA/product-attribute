# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging
import os
from datetime import datetime
import socket

from odoo import api, fields, models
from odoo import tools
from odoo.tools import image_resize_image

_logger = logging.getLogger(__name__)

try:
    from ftplib import FTP
except ImportError:
    _logger.error(
        "Cannot import 'ftplib' Python Librairy. 'product_to_scale_bizerba'"
        " module will not work properly."
    )


class ProductScaleLog(models.Model):
    _name = 'product.scale.log'
    _inherit = ['mail.activity.mixin']
    _order = 'log_date desc, id desc'

    _EXTERNAL_SIZE_ID_RIGHT = 4

    _DELIMITER = '#'

    _ACTION_SELECTION = [
        ('create', 'Creation'),
        ('write', 'Update'),
        ('unlink', 'Deletion'),
    ]

    _ACTION_MAPPING = {
        'create': 'C',
        'write': 'C',
        'unlink': 'S',
    }

    _ENCODING_MAPPING = {
        'iso-8859-1': '\r\n',
        'cp1252': '\n',
        'utf-8': '\n',
    }

    _TRANSLATED_TERM = {
        0x2018: 0x27,
        0x2019: 0x27,
        0x201C: 0x22,
        0x201D: 0x22
    }

    _EXTERNAL_TEXT_ACTION_CODE = 'C'

    _EXTERNAL_TEXT_DELIMITER = '#'

    # Private Section
    @api.multi
    def _clean_value(self, value, product_line):
        if not value:
            return ''
        elif product_line.multiline_length:
            res = ''
            current_val = value
            while current_val:
                res += current_val[:product_line.multiline_length]
                current_val = current_val[product_line.multiline_length:]
                if current_val:
                    res += product_line.multiline_separator
        else:
            res = value
        if product_line.delimiter:
            return res.replace(product_line.delimiter, '')
        else:
            return res

    @api.multi
    def _generate_external_text(self, value, product_line, external_id, log):
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,                    # WALO Code
            log.product_id.scale_group_id.external_identity,    # ABNR Code
            external_id,                                        # TXNR Code
            self._clean_value(value, product_line),             # TEXT Code
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    # Compute Section
    @api.depends('product_id', 'product_id.scale_group_id')
    def _compute_text(self):
        for log in self:
            group = log.product_id.scale_group_id
            product_text =\
                self._ACTION_MAPPING[log.action] + self._DELIMITER
            external_texts = []

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                if product_line.field_id:
                    value = getattr(log.product_id, product_line.field_id.name)

                if product_line.type == 'id':
                    product_text += str(log.product_id.id)

                elif product_line.type == 'numeric':
                    value = tools.float_round(
                        value * product_line.numeric_coefficient,
                        precision_rounding=product_line.numeric_round)
                    product_text += str(value).replace('.0', '')

                elif product_line.type == 'text':
                    product_text += self._clean_value(value, product_line)

                elif product_line.type == 'external_text':
                    external_id = str(log.product_id.id)\
                        + str(product_line.id).rjust(
                            self._EXTERNAL_SIZE_ID_RIGHT, '0')
                    external_texts.append(self._generate_external_text(
                        value, product_line, external_id, log))
                    product_text += external_id

                elif product_line.type == 'constant':
                    product_text += self._clean_value(
                        product_line.constant_value, product_line)

                elif product_line.type == 'external_constant':
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)

                    external_texts.append(self._generate_external_text(
                        product_line.constant_value, product_line, external_id,
                        log))
                    product_text += external_id

                elif product_line.type == 'many2one':
                    # If the many2one is defined
                    if value and not product_line.related_field_id:
                        product_text += value.id
                    elif value and product_line.related_field_id:
                        item_value = getattr(
                            value, product_line.related_field_id.name)
                        product_text +=\
                            item_value and str(item_value) or ''

                elif product_line.type == 'many2many':
                    # Select one value, depending of x2many_range
                    if product_line.x2many_range < len(value):
                        item = value[product_line.x2many_range - 1]
                        if product_line.related_field_id:
                            item_value = getattr(
                                item, product_line.related_field_id.name)
                        else:
                            item_value = item.id
                        product_text += self._clean_value(
                            item_value, product_line)

                elif product_line.type == 'product_image':
                    product_text += \
                        self._generate_image_file_name(
                            log.product_id, product_line.field_id,
                            product_line.suffix or '.PNG'
                        )

                if product_line.delimiter:
                    product_text += product_line.delimiter
            break_line = self._ENCODING_MAPPING[log.scale_system_id.encoding]
            log.product_text = product_text + break_line
            log.external_text = break_line.join(external_texts) + break_line
            log.external_text_display = '\n'.join(
                [x.replace('\n', '') for x in external_texts]
            )

    # Column Section
    log_date = fields.Datetime('Log Date', required=True)
    scale_system_id = fields.Many2one(
        'product.scale.system',
        string='Scale System', required=True
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )
    product_text = fields.Text(
        compute="_compute_text",
        string='Product Text',
        store=True
    )
    external_text = fields.Text(
        compute="_compute_text",
        string='External Text',
        store=True)
    external_text_display = fields.Text(
        compute="_compute_text",
        string='External Text (Display)',
        store=True
    )
    action = fields.Selection(
        _ACTION_SELECTION,
        string='Action', required=True
    )
    sent = fields.Boolean(string='Is Sent')
    last_send_date = fields.Datetime('Last Send Date')

    @api.multi
    def ftp_connection_open(self, scale_system):
        """Return a new FTP connection with found parameters."""
        _logger.info("Trying to connect to ftp://%s@%s:%d" % (
            scale_system.ftp_login, scale_system.ftp_host,
            scale_system.ftp_port))
        try:
            ftp = FTP(timeout=30)
            ftp.connect(scale_system.ftp_host, scale_system.ftp_port)
            if scale_system.ftp_login:
                ftp.login(
                    scale_system.ftp_login,
                    scale_system.ftp_password)
            else:
                ftp.login()
            return ftp
        except Exception:
            _logger.error("Connection to ftp://%s@%s:%d failed." % (
                scale_system.ftp_login, scale_system.ftp_host,
                scale_system.ftp_port))
            return False

    @api.multi
    def ftp_connection_close(self, ftp):
        try:
            ftp.quit()
        except Exception:
            pass

    def ftp_connection_push_text_file(
            self, ftp, distant_folder_path, local_folder_path,
            pattern, lines, encoding):
        if lines:
            # Generate temporary file
            f_name = datetime.now().strftime(pattern)
            local_path = os.path.join(local_folder_path, f_name)
            distant_path = os.path.join(distant_folder_path, f_name)
            f = open(local_path, 'wb')
            for line in lines:
                raw_text = line
                if encoding != 'utf-8':
                    raw_text = raw_text.translate(self._TRANSLATED_TERM)
                f.write(raw_text.encode(encoding, errors='ignore'))
            f.close()

            # Send File by FTP
            f = open(local_path, 'rb')
            ftp.storbinary('STOR ' + distant_path, f)
            f.close()
            # Delete temporary file
            os.remove(local_path)

    def ftp_connection_push_image_file(self, ftp,
                                       distant_folder_path, local_folder_path,
                                       obj, field, extension):

        # Generate temporary image file
        f_name = self._generate_image_file_name(obj, field, extension)
        if not f_name:
            # No image define
            return False
        local_path = os.path.join(local_folder_path, f_name)
        distant_path = os.path.join(distant_folder_path, f_name)
        image_base64 = getattr(obj, field.name)
        # Resize and save image
        ext = extension.replace('.', '')
        image_resize_image(
            base64_source=image_base64, size=(120, 120), encoding='base64',
            filetype=ext)
        image_data = base64.b64decode(image_base64)
        f = open(local_path, 'wb')
        f.write(image_data)
        f.close()

        # Send File by FTP
        f = open(local_path, 'rb')
        ftp.storbinary('STOR ' + distant_path, f)
        f.close()
        # Delete temporary file
        os.remove(local_path)

    @api.multi
    def send_log(self):
        config_obj = self.env['ir.config_parameter']
        folder_path = config_obj.sudo().get_param('bizerba.local_folder_path')

        system_map = {}
        for log in self:
            if log.scale_system_id in list(system_map.keys()):
                system_map[log.scale_system_id].append(log)
            else:
                system_map[log.scale_system_id] = [log]

        for scale_system, logs in system_map.items():

            # Open FTP Connection
            ftp = self.ftp_connection_open(logs[0].scale_system_id)
            if not ftp:
                return False

            # Generate and Send Files
            product_text_lst = []
            external_text_lst = []

            for log in logs:
                if log.product_text:
                    product_text_lst.append(log.product_text)
                if log.external_text:
                    external_text_lst.append(log.external_text)

            # Push First Image for constrains reason
            # Image extension will get on the line field suffix
            # for default will be `png` if suffix empty.
            for product_line in scale_system.product_line_ids:
                if product_line.type == 'product_image' and scale_system.send_images:
                    # send product image
                    self.ftp_connection_push_image_file(
                        ftp,
                        scale_system.product_image_relative_path,
                        folder_path, log.product_id,
                        product_line.field_id,
                        product_line.suffix or '.PNG'
                    )

            self.ftp_connection_push_text_file(
                ftp,
                scale_system.csv_relative_path,
                folder_path, scale_system.external_text_file_pattern,
                external_text_lst, scale_system.encoding
            )
            self.ftp_connection_push_text_file(
                ftp,
                scale_system.csv_relative_path,
                folder_path, scale_system.product_text_file_pattern,
                product_text_lst, scale_system.encoding
            )

            # Close FTP Connection
            self.ftp_connection_close(ftp)

            # Mark logs as sent
            for log in logs:
                log.write({'sent': True, 'last_send_date': fields.Datetime.now()})
        return True

    @api.multi
    def cron_send_to_scale(self):
        log_ids = self.search([('sent', '=', False)], order='log_date')
        try:
            log_ids.send_log()
        except socket.timeout:
            _logger.debug("Timed out while sending logs to scale. Will try again at next run.")

    @api.multi
    def _generate_image_file_name(self, obj, field, extension):
        if getattr(obj, field.name):
            return "%d%s" % (obj.id, extension)
        else:
            return ''
