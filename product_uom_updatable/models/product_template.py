# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import groupby

from psycopg2 import sql

from odoo import _, models
from odoo.exceptions import UserError


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
        sorted_items = sorted(self, key=lambda r: r[field_name])
        for key, products_group in groupby(sorted_items, key=lambda r: r[field_name]):
            product_ids = [product.id for product in products_group]
            new_uom = uom_obj.browse(uom_id)
            if (
                key.category_id == new_uom.category_id
                and key.factor_inv == new_uom.factor_inv
            ):
                # pylint: disable=sql-injection
                query = sql.SQL(
                    "UPDATE product_template SET {field} = %s WHERE id in %s"
                ).format(field=sql.Identifier(field_name))
                self.env.cr.execute(query, (new_uom.id, tuple(product_ids)))
                self.invalidate_cache(fnames=[field_name], ids=product_ids)
            else:
                raise UserError(
                    _(
                        "You can not change the unit of measure of a product "
                        "to a new unit that doesn't have the same category "
                        "and factor"
                    )
                )
