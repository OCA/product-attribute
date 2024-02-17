# © 2014 Today Akretion
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models
from odoo.models import LOG_ACCESS_COLUMNS


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
        store=True,
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

    def write(self, vals):
        # OVERRIDE to supress LOG_ACCESS_COLUMNS writes if we're only writing on quick
        # magic fields, as they could lead to concurrency issues.
        #
        # Moreover, from a functional perspective, these magic fields aren't really
        # modifying the product's data so it doesn't make sense to update its metadata.
        #
        # We achieve it by stopping the ``write`` [^1] to modify LOG_ACCESS_COLUMNS.
        # By changing the log access rights ``_log_access``
        #
        # [^1]:
        # https://github.com/odoo/odoo/blob/dab802a939c97603f70c504e98ecc92b0ac552f9/odoo/models.py#L3677C1-L3679C61 # noqa: B950
        #
        # Basically, if all we're modifying are quick magic fields, and we don't have
        # any other column to flush besides the LOG_ACCESS_COLUMNS, clear it.
        quick_fnames = ("qty_to_process", "quick_uom_id")
        if self and any(quick_fname in vals.keys() for quick_fname in quick_fnames):
            cr = self.env.cr
            Model = self._build_model(self.pool, cr)
            Model._auto = False
            Model._log_access = set(list([]))
        res = super(ProductProduct, self).write(vals)
        if not self._log_access:
            cr = self.env.cr
            Model = self._build_model(self.pool, cr)
            Model._auto = True
            Model._log_access = set(LOG_ACCESS_COLUMNS)
        return res

    @property
    def pma_parent(self):
        # shorthand for product_mass_addition parent
        parent_model = self.env.context.get("parent_model")
        parent_id = self.env.context.get("parent_id")
        if parent_model and parent_id:
            return self.env[parent_model].browse(parent_id)

    def _default_quick_uom_id(self):
        raise NotImplementedError()

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
