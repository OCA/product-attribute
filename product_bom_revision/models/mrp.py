# Copyright 2019 C2i Change 2 improve - Eduardo Magdalena <emagdalena@c2i.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_revision = fields.Char(string="Revision")

    @api.multi
    def name_get(self):
        result = []
        for bom in self:
            rec_name = "%s %s" % (
                _("[Rev. %s]") % bom.bom_revision if bom.bom_revision else '',
                bom.product_tmpl_id.name,
            )
            result.append((bom.id, rec_name))
        return result
