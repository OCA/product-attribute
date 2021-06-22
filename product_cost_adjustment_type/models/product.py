# Copyright 2021 - Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _change_price(self, new_price, account):
        """Helper to create the stock valuation layers and the account moves
        after an update of standard price.
        :param new_price: new standard price
        """
        # Check Access Rights for Journal Entry creation.
        if not self.env["stock.valuation.layer"].check_access_rights(
            "read", raise_exception=False
        ):
            raise UserError(
                _(
                    """You cannot post the cost of a product as it leads to the
                     creation of a journal entry, for which you don't have the
                     access rights."""
                )
            )

        svl_vals_list = []
        company_id = self.env.company
        for product in self:
            if product.cost_method not in ("standard", "average"):
                continue
            quantity_svl = product.sudo().quantity_svl
            if float_is_zero(quantity_svl, precision_rounding=product.uom_id.rounding):
                continue
            diff = new_price - product.standard_price
            value = company_id.currency_id.round(quantity_svl * diff)
            if company_id.currency_id.is_zero(value):
                continue

            svl_vals = {
                "company_id": company_id.id,
                "product_id": product.id,
                "description": _(
                    "Product value modified by cost adjustment (from %s to %s)"
                )
                % (product.standard_price, new_price),
                "value": value,
                "quantity": 0,
            }
            svl_vals_list.append(svl_vals)
        stock_valuation_layers = (
            self.env["stock.valuation.layer"].sudo().create(svl_vals_list)
        )

        # Handle account moves.
        product_accounts = {
            product.id: product.product_tmpl_id.get_product_accounts()
            for product in self
        }
        am_vals_list = []
        for stock_valuation_layer in stock_valuation_layers:
            product = stock_valuation_layer.product_id
            value = stock_valuation_layer.value

            # Sanity check.
            if not account:
                raise UserError(
                    _("You must set an account on your cost adjustment type.")
                )
            if not product_accounts[product.id].get("stock_valuation"):
                raise UserError(
                    _(
                        """You don't have any stock valuation account defined on your
                         product category. You must define one before processing this
                         operation."""
                    )
                )

            if value < 0:
                debit_account_id = account.id
                credit_account_id = product_accounts[product.id]["stock_valuation"].id
            else:
                debit_account_id = product_accounts[product.id]["stock_valuation"].id
                credit_account_id = account.id

            move_vals = {
                "journal_id": product_accounts[product.id]["stock_journal"].id,
                "company_id": company_id.id,
                "ref": product.default_code,
                "stock_valuation_layer_ids": [(6, None, [stock_valuation_layer.id])],
                "move_type": "entry",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": _(
                                "%(user)s changed cost from %(previous)s to %(new_price)s - %(product)s",
                                user=self.env.user.name,
                                previous=product.standard_price,
                                new_price=new_price,
                                product=product.display_name,
                            ),
                            "account_id": debit_account_id,
                            "debit": abs(value),
                            "credit": 0,
                            "product_id": product.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": _(
                                "%(user)s changed cost from %(previous)s to %(new_price)s - %(product)s",
                                user=self.env.user.name,
                                previous=product.standard_price,
                                new_price=new_price,
                                product=product.display_name,
                            ),
                            "account_id": credit_account_id,
                            "debit": 0,
                            "credit": abs(value),
                            "product_id": product.id,
                        },
                    ),
                ],
            }
            am_vals_list.append(move_vals)
            product.write({"standard_price": new_price})
        account_moves = self.env["account.move"].sudo().create(am_vals_list)
        if account_moves:
            account_moves._post()
