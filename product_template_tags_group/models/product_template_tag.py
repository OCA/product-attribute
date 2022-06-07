#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplateTag (models.Model):
    _inherit = 'product.template.tag'

    tag_group_id = fields.Many2one(
        comodel_name='product.template.tag.group',
        string="Group",
    )

    @api.multi
    def name_get(self):
        res = super().name_get()
        id_names_list = list()
        for tag_id, tag_name in res:
            tag = self.browse(tag_id)
            group = tag.tag_group_id
            if group:
                tag_name = "{group_name}: {tag_name}".format(
                    group_name=group.display_name,
                    tag_name=tag_name
                )
            id_names_list.append((tag_id, tag_name))
        return id_names_list
