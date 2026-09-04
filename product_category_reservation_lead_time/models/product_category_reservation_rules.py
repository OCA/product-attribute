from odoo import api, fields, models


class ProductCategoryReservationRule(models.Model):
    _name = "product.category.reservation.rule"
    _description = "Product Category Reservation Lead Time Rule"
    _order = "company_id, category_id"

    category_id = fields.Many2one(
        "product.category",
        string="Product Category",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    reservation_days = fields.Integer(
        string="Reservation Lead Time (days)",
        required=True,
        help="Number of days before the delivery date within which the line "
        "enters the reservation window. 0 = reserve only on the delivery date.",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "category_company_uniq",
            "unique(category_id, company_id)",
            "A reservation lead time rule already exists for this category "
            "and company",
        ),
        (
            "reservation_days_positive",
            "check(reservation_days >= 0)",
            "The reservation lead time cannot be negative.",
        ),
    ]

    @api.model
    def _resolve_reservation_days(self, category, company):
        """Resolve the reservation lead time (days) for a category and company.

        1) walk up the category hierarchy (parent_id) from the most specific
           one and return the first active matching rule
        2) If not category in the chain has a rule, fall back to the company
           global lead time (res.company.reservation_lead_days)

        Row existence is the discriminator: a rule means configured (0
        included); no rule in the whole chain means fall back to the global.
        """
        if not company:
            company = self.env.company
        # Category chain, from the most specific to the root
        chain = []
        categ = category
        while categ:
            chain.append(categ.id)
            categ = categ.parent_id
        if chain:
            rules = self.search(
                [
                    ("company_id", "=", company.id),
                    ("category_id", "in", chain),
                ]
            )
            by_categ = {r.category_id.id: r.reservation_days for r in rules}
            for categ_id in chain:
                if categ_id in by_categ:
                    return by_categ[categ_id]
        return company.reservation_lead_days
