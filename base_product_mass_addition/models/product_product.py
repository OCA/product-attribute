# © 2014 Today Akretion
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    qty_to_process = fields.Float(
        compute="_compute_process_qty",
        inverse="_inverse_set_process_qty",
        help="Set this quantity to create a new line "
        "for this product or update the existing one.",
    )
    quick_uom_category_id = fields.Many2one(
        "uom.category", related="quick_uom_id.category_id"
    )
    quick_uom_id = fields.Many2one(
        "uom.uom",
        domain="[('category_id', '=', quick_uom_category_id)]",
        compute="_compute_quick_uom_id",
        inverse="_inverse_set_process_qty",
    )

    def _inverse_set_process_qty(self):
        parent = self.pma_parent
        if parent:
            for product in self:
                quick_line = parent._get_quick_line(product)
                if quick_line:
                    parent._update_quick_line(product, quick_line)
                else:
                    parent._add_quick_line(product, quick_line._name)

    @property
    def pma_parent(self):
        # shorthand for product_mass_addition parent
        parent_model = self.env.context.get("parent_model")
        parent_id = self.env.context.get("parent_id")
        if parent_model and parent_id:
            return self.env[parent_model].browse(parent_id)

    def _default_quick_uom_id(self):
        raise NotImplementedError

    def _compute_quick_uom_id(self):
        parent = self.pma_parent
        if parent:
            for rec in self:
                quick_line = parent._get_quick_line(rec)
                if quick_line:
                    rec.quick_uom_id = quick_line.product_uom
                else:
                    rec.quick_uom_id = rec._default_quick_uom_id()

    def _compute_process_qty(self):
        if not self.pma_parent:
            return

    def button_quick_open_product(self):
        self.ensure_one()
        return {
            "name": self.display_name,
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }
