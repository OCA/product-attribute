from odoo import api, models
from odoo.fields import Domain


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _search_display_name(self, operator, value):
        """Extends the "display_name" search to also match the code
        supplier (product.supplierinfo.product_code), on all
        supplier lines of the product.
        """
        domain = super()._search_display_name(operator, value)

        # We want to be able to search by supplier code from anywhere.
        # We therefore systematically searches on seller_ids.product_code, except
        # if a supplier partner is already present in the context
        # (in this case, Odoo already natively do the job).
        partner_id = self.env.context.get("partner_id", False)
        partner = self.env["res.partner"].browse(partner_id)
        if not partner.supplier_rank:
            # if partner is not a supplier
            extra_domain = [
                ("product_tmpl_id.seller_ids.product_code", operator, value)
            ]
            # NEGATIVE_OPERATORS are : not ... in/like, !=
            is_positive = operator not in Domain.NEGATIVE_OPERATORS
            if is_positive:
                domain = Domain.OR([domain, extra_domain])
            else:
                domain = Domain.AND([domain, extra_domain])
        return domain
