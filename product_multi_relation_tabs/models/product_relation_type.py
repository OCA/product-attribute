# Copyright 2014-2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=no-self-use
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResProductRelationType(models.Model):
    # pylint: disable=too-few-public-methods
    _inherit = 'product.relation.type'

    tab_id_left = fields.Many2one(
        comodel_name='product.tab',
        string='Tab for this relation',
        help="Tab in which these relations will be visible on product.")
    tab_id_right = fields.Many2one(
        comodel_name='product.tab',
        string='Tab for inverse relation',
        help="Tab in which inverse relations will be visible on product.")

    @api.multi
    @api.constrains(
        'product_type_left',
        'product_category_left',
        'tab_id_left')
    def _check_tab_left(self):
        """Conditions for left product should be consistent with tab."""
        for rec in self:
            if not rec.tab_id_left:
                continue
            tab_product_type = rec.tab_id_left.product_type
            if tab_product_type and tab_product_type != rec.product_type_left:
                raise ValidationError(_(
                    "Product type left not compatible with left tab"))
            tab_product_category_id = rec.tab_id_left.product_category_id
            if tab_product_category_id and \
                    tab_product_category_id != rec.product_category_left:
                raise ValidationError(_(
                    "Product category left not compatible with left tab"))

    @api.multi
    @api.constrains(
        'product_type_right',
        'product_category_right',
        'tab_id_right')
    def _check_tab_right(self):
        """Conditions for right product should be consistent with tab."""
        for rec in self:
            if not rec.tab_id_right:
                continue
            tab_product_type = rec.tab_id_right.product_type
            if tab_product_type and tab_product_type != rec.product_type_right:
                raise ValidationError(_(
                    "Product type right not compatible with right tab"))
            tab_product_category_id = rec.tab_id_right.product_category_id
            if tab_product_category_id and \
                    tab_product_category_id != rec.product_category_right:
                raise ValidationError(_(
                    "Product category right not compatible with right tab"))
