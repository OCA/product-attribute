# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    @api.model
    def get_category_sequence_id(self, category=False):
        if self.env.user.company_id.use_parent_categories_to_determine_prefix:
            while not category.sequence_id and category.parent_id:
                category = category.parent_id
        return category.sequence_id or self.env.ref("product_sequence.seq_product_auto")

    @api.constrains("prefix")
    def _check_prefix_product_category(self):
        if self.env.context.get("_no_sequence_prefix_check"):
            return
        for rec in self:
            categs = self.env["product.category"].search([("sequence_id", "=", rec.id)])
            if not categs:
                continue
            if any(categ.code_prefix != rec.prefix for categ in categs):
                raise ValidationError(
                    _(
                        "Sequence %(seq_name)s is used on following product "
                        "categories and prefix cannot be changed here:"
                        "\n%(categ_names)s"
                    )
                    % dict(
                        seq_name=rec.name,
                        categ_names="\n -".join(categs.mapped("name")),
                    )
                )
