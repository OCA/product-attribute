# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductDocumentationSet(models.Model):

    _name = "product.doc.set"
    _description = "Product Documentation Set"

    name = fields.Char(required=True)
    product_ids = fields.Many2many("product.template")
    category_ids = fields.Many2many("product.category")
    usage = fields.Selection(
        [("internal", "Internal Reference")],
        string="Usage",
        help="The purpose for this list of documents.",
    )
    country_ids = fields.Many2many("res.country", string="Countries")
    lang = fields.Selection(
        lambda self: self.env["res.lang"].get_installed(), string="Language"
    )
    active = fields.Boolean("Active?", default=True)
    attachment_ids = fields.Many2many("ir.attachment", string="Documents")
    notes = fields.Html()

    @api.model
    def get_usage_document_sets(
        self, usage, country=None, lang=None, product=None, category=None
    ):
        """
        Find the Document Sets for a single Product Category,
        filtering by the particular Usage, Country and Language.

        Search will only be performed on the parameters given
        (Country and or Lang).

        The search is also done following the chain of parent Categories,
        until a Document Set is found.

        :param usage:       Usage selection option (required)
        :param country:     Country record (optional)
        :param lang:        Language selection option (optional)
        :param product:     Product record to search on (optional)
        :param category:    Product Category record to search on (optional)

        :returns:           a recordset of Product Documentation Sets
        """
        domain = [("usage", "=", usage)]
        if country:
            country.ensure_one()
            domain.append(("country_ids", "in", country.id))
        if lang:
            domain.append(("lang", "=", lang))

        if product:
            product.ensure_one()
            domain.append(("product_ids", "in", product.id))
        if category:
            category.ensure_one()
            domain.append(("category_ids", "in", category.id))

        document_sets = self.search(domain)

        if not document_sets:
            # Try again for the Product's Category
            product_categ = product and product.categ_id
            if product_categ:
                document_sets = self.get_usage_document_sets(
                    usage, country, lang, category=product_categ
                )
        if not document_sets:
            # Try again for the Parent Category (recursively
            parent_categ = category and category.parent_id
            if parent_categ:
                document_sets = self.get_usage_document_sets(
                    usage, country, lang, category=parent_categ
                )
        return document_sets
