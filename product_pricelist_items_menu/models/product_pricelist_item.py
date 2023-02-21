from odoo import _, fields, models
from odoo.exceptions import UserError

from ..constants import constants


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    width_from = fields.Float(
        string="Width from (mm)",
        help="Width from",
    )

    width_to = fields.Float(
        string="Width to (mm)",
        help="Width to",
    )

    height_from = fields.Float(
        string="Height from (mm)",
        help="Height from",
    )

    height_to = fields.Float(
        string="Height to (mm)",
        help="Height to",
    )

    use_dim_rules = fields.Boolean(
        string="Use dimension rules",
        help="Use dimension rules",
        default=False,
    )

    def write(self, values):
        dim_from_dict = dict(
            filter(
                lambda elem: "_from" in elem[0]
                and elem[1] < constants.PRICELIST_ITEM_MINIMAL_FROM,
                values.items(),
            )
        )
        if dim_from_dict:
            raise UserError(
                _("""One of the dimensions values "from" must be at least %s """)
                % constants.PRICELIST_ITEM_MINIMAL_FROM
            )
        return super().write(values)
