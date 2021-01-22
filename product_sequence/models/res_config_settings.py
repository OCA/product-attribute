# Copyright 2004 Tiny SPRL
# Copyright 2016 Sodexis
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_parent_categories_to_determine_prefix = fields.Boolean(
        related="company_id.use_parent_categories_to_determine_prefix",
        readonly=False,
    )
