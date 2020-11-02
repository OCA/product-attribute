# -*- coding: utf-8 -*-
# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import groupby

from odoo import _, api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def write(self, vals):
        uom_id = vals.pop("uom_id", False)
        uom_po_id = vals.pop("uom_po_id", False)
        res = super(ProductTemplate, self).write(vals)
        if uom_id:
            self._update_uom(uom_id)
        if uom_po_id:
            self._update_uom_po(uom_po_id)
        return res

    def _update_uom(self, uom_id):
        uom_obj = self.env["uom.uom"]
        for key, products_group in groupby(self, key=lambda r: r.uom_id):
            product_list = list(products_group)
            product_id_list = []
            for product in product_list:
                product_id_list.append(product.id)
            new_uom = uom_obj.browse(uom_id)
            if key.category_id == new_uom.category_id and key.factor_inv == new_uom.factor_inv:
                self.env.cr.execute(
                    "UPDATE product_template SET uom_id = %(uom)s WHERE id in %(product_id)s",
                    {"uom": new_uom.id, "product_id": tuple(product_id_list)},
                )
            else:
                raise UserError(
                    _(
                        "You can not change the unit of measure of a product to a new unit that doesn't have the same category and factor"
                    )
                )

    def _update_uom_po(self, uom_po_id):
        uom_obj = self.env["uom.uom"]
        for key, products_group in groupby(self, key=lambda r: r.uom_po_id):
            product_list = list(products_group)
            product_id_list = []
            for product in product_list:
                product_id_list.append(product.id)
            new_uom_po = uom_obj.browse(uom_po_id)
            if (
                key.category_id == new_uom_po.category_id
                and key.factor_inv == new_uom_po.factor_inv
            ):
                self.env.cr.execute(
                    "UPDATE product_template SET uom_po_id = %(uom)s WHERE id in %(product_id)s",
                    {"uom": new_uom_po.id, "product_id": tuple(product_id_list)},
                )
            else:
                raise UserError(
                    _(
                        "You can not change the purchase unit of measure of a product to a new unit that doesn't have the same category and factor"
                    )
                )
