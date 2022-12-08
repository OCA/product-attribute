from odoo import api, fields, models


class ProductCustomerInfo(models.Model):
    """Need to restore default fields definition, as in product.supplierinfo"""

    _inherit = "product.customerinfo"

    group_id = fields.Many2one("product.supplierinfo.group", required=False)
    company_id = fields.Many2one(
        "res.company",
        "Company",
        default=lambda self: self.env.company.id,
        index=1,
        related=False,
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product Template",
        check_company=True,
        index=True,
        ondelete="cascade",
        related=False,
    )
    name = fields.Many2one(
        "res.partner",
        "Vendor",
        ondelete="cascade",
        required=True,
        check_company=True,
        related=False,
    )
    product_id = fields.Many2one(
        "product.product", "Product Variant", check_company=True, related=False
    )
    product_name = fields.Char(
        "Vendor Product Name",
        related=False,
    )
    product_code = fields.Char(
        "Vendor Product Code",
        related=False,
    )
    sequence = fields.Integer("Sequence", default=1, related=False)

    @api.model_create_multi
    def create(self, list_vals):
        return super(
            ProductCustomerInfo, self.with_context(skip_group_specific=True)
        ).create(list_vals)
