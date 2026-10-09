# Copyright 2023 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    specific_supplierinfo_group_ids = fields.One2many(
        "product.supplierinfo.group",
        "product_id",
        name="Specific Vendor",
        help="This supplier group only apply to the current variant",
    )

    def write(self, vals):
        """Write supplierinfo_group_ids commands on the template, not on the variant.

        As supplierinfo_group_ids is stored on product.template but is a
        non-stored related field on product.product, writing the commands on
        the variant raises two issues:
        - a create command is lost: another update command (setting
          product_tmpl_id) invalidates the cache and drops the created group;
        - an unlink command is played twice: the first unlink already hits
          the database, and the framework re-plays the whole write once the
          related cache is invalidated.

        Writing the stored field on the template fixes both issues.
        """
        if "supplierinfo_group_ids" in vals:
            vals = dict(vals)
            supplierinfo_group_commands = vals.pop("supplierinfo_group_ids")
            self.product_tmpl_id.write(
                {"supplierinfo_group_ids": supplierinfo_group_commands}
            )
        return super().write(vals)
