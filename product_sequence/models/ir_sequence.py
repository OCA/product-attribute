# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    @api.model
    def get_category_sequence_id(self, category=False):
        if self.env.user.company_id.use_parent_categories_to_determine_prefix:
            while category and not category.sequence_id and category.parent_id:
                category = category.parent_id
        return category.sequence_id or self.env.ref("product_sequence.seq_product_auto")
