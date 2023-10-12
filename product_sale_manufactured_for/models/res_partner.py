# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from collections import defaultdict

from odoo import _, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        res = super().write(vals)
        if vals.get("active") is False:
            self._clean_product_manufactured_for()
        return res

    def _clean_product_manufactured_for(self):
        """Update product manufactured for when a partner is archived.

        When a partner being archived is used on the Manufactured For field
        that information is not visible anymore on the product form, although it
        is still set.
        And that product can still not be ordered by any other customers.

        Removing this relation when a partner is being archived solves the issue.

        The change is also being logged in the chatter of the related product.

        """
        query = (
            "DELETE FROM product_product_manuf_for_partner_rel "
            "WHERE partner_id IN %s"
            "RETURNING "
            "    product_product_manuf_for_partner_rel.product_id, "
            "    product_product_manuf_for_partner_rel.partner_id;"
        )
        self.env.cr.execute(query, (tuple(self.ids),))
        result = self.env.cr.fetchall()
        if result:
            product_to_update = defaultdict(list)
            for row in result:
                product_to_update[row[0]].append(row[1])
            products = self.env["product.product"].browse(product_to_update.keys())
            customer_ids = {
                id for values in product_to_update.values() for id in values
            }
            all_customers = self.env["res.partner"].browse(customer_ids)
            for product in products:
                customers = all_customers.filtered(
                    lambda customer: customer.id in product_to_update[product.id]
                )
                customers_name = ", ".join(customers.mapped("name"))
                product.message_post(
                    body=_(
                        "The product was manufactured for %(customers_name)s "
                        "but the customer(s) has been archived."
                    )
                    % {"customers_name": customers_name}
                )
