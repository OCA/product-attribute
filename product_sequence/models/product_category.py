# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code_prefix = fields.Char(
        string="Prefix for Product Internal Reference",
        help="Prefix used to generate the internal reference for products "
             "created with this category. If blank the "
             "default sequence will be used.",
        company_dependent=True,
    )
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence", string="Product Sequence",
        help="This field contains the information related to the numbering "
             "of the journal entries of this journal.",
        copy=False, readonly=True,
    )

    @api.model
    def _get_existing_sequence(self, prefix, company=False):
        """Tries to find a valid sequence for the given prefix and company
        (optional)
        :param prefix: a string with the prefix of the sequence.
        :param company: a res.company record.
        :return: a single ir.sequence record or the empty model.
        """
        domain = [
            ('prefix', '=', prefix),
            ('code', 'ilike', 'product.product')
        ]
        if company:
            domain.extend([
                '|',
                ('company_id', '=', company.id),
                ('company_id', '=', False),
            ])
        return self.env["ir.sequence"].search(
            domain, limit=1, order="company_id")

    @api.model
    def _prepare_ir_sequence(self, prefix, company=False):
        """Prepare the vals for creating the sequence
        :param prefix: a string with the prefix of the sequence.
        :param company: a res.company record.
        :return: a dict with the values.
        """
        vals = {
            "name": "Product " + prefix,
            "code": "product.product - " + prefix,
            "padding": 5,
            "prefix": prefix,
        }
        if company:
            vals["company_id"] = company.id
        return vals

    @api.model
    def _get_default_company(self):
        return self.env.user.company_id

    @api.multi
    def write(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            sequence = self._get_existing_sequence(
                prefix, company=self._get_default_company())
            if not sequence:
                seq_vals = self._prepare_ir_sequence(
                    prefix, company=self._get_default_company())
                sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            sequence = self._get_existing_sequence(
                prefix, company=self._get_default_company())
            if not sequence:
                seq_vals = self._prepare_ir_sequence(
                    prefix, company=self._get_default_company())
                sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().create(vals)
