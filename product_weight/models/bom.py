# -*- coding: utf-8 -*-
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.multi
    def get_final_components(self):
        bom_lines = []
        for line in self:
            if not line.child_line_ids:
                bom_lines.append(line)
            else:
                bom_lines += line.child_line_ids.get_final_components()
        return bom_lines
