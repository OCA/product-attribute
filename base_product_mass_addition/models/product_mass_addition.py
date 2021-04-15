# © 2019 Today Akretion
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ProductMassAddition(models.AbstractModel):
    _name = "product.mass.addition"
    _description = "inherit this to add a mass product addition function\
                    to your model"

    @api.model
    def _common_action_keys(self):
        """Call it in your own child module"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "target": "current",
            "context": {
                "parent_id": self.id,
                "parent_model": self._name,
            },
            "view_mode": "tree",
        }

    def _prepare_quick_line(self, product):
        res = self._get_quick_line_qty_vals(product)
        res.update({"product_id": product.id})
        return res

    def _get_quick_line(self, product):
        raise NotImplementedError

    def _add_quick_line(self, product, lines_key=""):
        if not lines_key:
            raise NotImplementedError
        vals = self._prepare_quick_line(product)
        vals = self._complete_quick_line_vals(vals)
        self.write({lines_key: [(0, 0, vals)]})

    def _update_quick_line(self, product, line):
        if product.qty_to_process:
            # apply the on change to update price unit if depends on qty
            vals = self._get_quick_line_qty_vals(product)
            vals["id"] = line.id
            vals = self._complete_quick_line_vals(vals)
            line.write(vals)
        else:
            line.unlink()

    def _get_quick_line_qty_vals(self, product):
        raise NotImplementedError

    def _complete_quick_line_vals(self, vals, lines_key=""):
        if not lines_key:
            raise NotImplementedError
        init_keys = ["product_id"]
        update_vals = {key: val for key, val in vals.items() if key not in init_keys}
        lines = getattr(self, lines_key)
        if "id" in vals:
            line = lines.filtered(lambda x: x.id == vals["id"])
            return line.play_onchanges(update_vals, list(update_vals.keys()))
        else:
            line = lines
            if len(lines) > 1:
                line = lines[0]
            return line.play_onchanges(vals, list(vals.keys()))
