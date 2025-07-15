from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    import_status = fields.Selection(
        [("new_or_updated", "New or Updated"), ("unchanged", "Unchanged")],
        default="unchanged",
    )
