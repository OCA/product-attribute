# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import groupby

from odoo import models
from odoo.exceptions import UserError
from odoo.tools import SQL


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        uom_id = vals.pop("uom_id", False)
        uom_po_id = vals.pop("uom_po_id", False)
        if uom_id:
            self._update_uom(uom_id, "uom_id")
        if uom_po_id:
            self._update_uom(uom_po_id, "uom_po_id")
        res = super().write(vals)
        return res

    def _update_uom(self, uom_id, field_name):
        uom_obj = self.env["uom.uom"]
        new_uom = uom_obj.browse(uom_id)
        sorted_items = sorted(self, key=lambda r: r[field_name])

        for key, products_group in groupby(sorted_items, key=lambda r: r[field_name]):
            product_ids = [p.id for p in products_group]

            if (
                key.category_id == new_uom.category_id
                and key.factor_inv == new_uom.factor_inv
            ):
                # pylint: disable=sql-injection
                self.env.cr.execute(
                    SQL(
                        """
                    UPDATE product_template
                    SET %(field)s = %(new_uom)s
                    WHERE id IN %(product_ids)s
                    """,
                        field=SQL.identifier(field_name),
                        new_uom=new_uom.id,
                        product_ids=tuple(product_ids),
                    )
                )
                products = self.env["product.template"].browse(product_ids)
                products.invalidate_recordset(fnames=[field_name])
            else:
                raise UserError(
                    self.env._(
                        "You cannot change the unit of measure of a product "
                        "to a new unit that doesn't have the same category "
                        "and factor"
                    )
                )
