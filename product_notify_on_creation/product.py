##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp.osv import fields, orm
from openerp.tools.translate import _
import tools

UID_ROOT = 1


class product_product(orm.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    def _send_mail_for_product(self, cr, uid, vals, context=None):
        """
        Send email when creating a new product
        """
        if context is None:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        email_to = self.pool.get('res.users').browse(cr, uid, uid).email
        user = self.pool.get('res.users').browse(cr, UID_ROOT, uid)
        if not user.email:
            raise orm.except_orm(
                _('Email Required'),
                _('The current user must have an email address configured '
                  'in User Preferences to be able to send outgoing emails.')
            )
        # Company informations
        company = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).company_id
        html_body = """
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
            <title>New Product</title>
            </head>
            <body>
            <table border="0" cellspacing="10" cellpadding="0" width="100%%"
                style="font-family: Arial, Sans-serif; font-size: 14">
                <tr>
                    <td width="100%%">
                        Hello, a new product has been created
                    </td>
                </tr>
                <tr>
                    <td width="100%%">Below are the details of product:</td>
                </tr>
            </table>

            <table cellspacing="0" cellpadding="5" border="0" summary=""
                style="width: 90%%; font-family: Arial, Sans-serif;
                border: 1px Solid #ccc; background-color: #f6f6f6">
                <tr valign="center" align="left">
                    <td bgcolor="DFDFDF">
                    <h3>%(name)s</h3>
                    </td>
                </tr>
                <tr>
                    <td>
                    <table cellpadding="8" cellspacing="0" border="0"
                        style="font-size: 14"  bgcolor="f6f6f6"
                        width="90%%">
                        <tr>
                            <td >
                            <b>Description:</b>%(description)s
                            </td>
                        </tr>
                    </table>
                    </td>
                </tr>
            </table>
            <br/><br/>
            <div style="width: 375px; margin: 0px; padding: 0px;
                background-color: #8E0000; border-top-left-radius: 5px 5px;
                border-top-right-radius: 5px 5px;
                background-repeat: repeat no-repeat;">
                    <h3 style="margin: 0px; padding: 2px 14px; font-size: 12px;
                        color: #DDD;">
                        <strong style="text-transform:uppercase;">
                        %(company_name)s
                    </strong>
                </h3>
            </div>
            <div style="width: 347px; margin: 0px; padding: 5px 14px;
                line-height: 16px; background-color: #F2F2F2;">
                <span style="color: #222; margin-bottom: 5px; display: block;">
                    %(company_street)s<br/>
                    %(company_street2)s<br/>
                    %(company_zip)s %(company_city)s<br/>
                    %(company_state_name)s<br/>
                </span>
                <div style="margin-top: 0px; margin-right: 0px;
                    margin-bottom: 0px; margin-left: 0px; padding-top: 0px;
                    padding-right: 0px; padding-bottom: 0px;
                    padding-left: 0px; ">
                    Phone:&nbsp; %(company_phone)s
                </div>
                <div>
                    Web :&nbsp;
                    <a href="%(company_website)s">%(company_website)s</a>
                </div>
            </div>
            </body>
            </html>
        """
        body_vals = {'name': vals.get('name'),
                     'description': vals.get('description') or '',
                     'company_name': company.name,
                     'company_street': company.street or '',
                     'company_street2': company.street2 or '',
                     'company_zip': company.zip or '',
                     'company_city': company.city or '',
                     'company_state_name': company.state_id and
                     company.state_id.name or company.country_id.name or '',
                     'company_phone': company.phone or '',
                     'company_website': company.website or ''}

        subject = "Odoo CubeP: New product"
        body = html_body % body_vals
        mail_id = mail_mail.create(cr, uid, {
            'email_from': user.email,
            'email_to': email_to,
            'subject': subject,
            'body_html': body}, context=context)
        mail_mail.send(cr, uid, [mail_id], context=context)

    def create(self, cr, uid, data, context=None):
        product_id = super(product_product, self).create(
            cr, uid, data, context=context
        )
        # Send email when creating a new product
        self._send_mail_for_product(cr, uid, data, context=context)
        return product_id
