# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


def RECS(recset):
    return [(6, 0, recset.mapped("id"))]


class TestProductDoc(TransactionCase):
    def setUp(self):
        """
        category1 ...........> docset1
         |_ category2
             |_ product1
             |_ product2 ....> docset2
        """
        super(TestProductDoc, self).setUp()
        ref = self.env.ref
        self.DocSet = self.env["product.doc.set"]
        self.Category = self.env["product.category"]
        self.Product = self.env["product.template"]

        self.category1 = self.Category.create({"name": "Category1"})
        self.category2 = self.Category.create(
            {"name": "Category2", "parent_id": self.category1.id}
        )

        self.product1 = self.Product.create(
            {"name": "Product1", "categ_id": self.category2.id}
        )
        self.product2 = self.Product.create(
            {"name": "Product2", "categ_id": self.category2.id}
        )

        self.docset1 = self.DocSet.create(
            {
                "name": "DocSet1",
                "usage": "internal",
                "lang": "en_US",
                "country_ids": RECS(ref("base.fr") + ref("base.be")),
                "category_ids": RECS(self.category1),
            }
        )
        self.docset2 = self.DocSet.create(
            {
                "name": "DocSet2",
                "usage": "internal",
                "lang": "en_US",
                "country_ids": RECS(ref("base.fr") + ref("base.be")),
                "product_ids": RECS(self.product2),
            }
        )

    def test_docset_from_parent_category(self):
        """Find DocSet from parent category"""
        docset = self.product1.get_usage_document_sets(
            "internal", country=self.env.ref("base.fr"), lang="en_US"
        )
        self.assertEqual(docset, self.docset1)

    def test_docset_from_product(self):
        """Find DocSet from Product Template"""
        docset = self.product2.get_usage_document_sets(
            "internal", country=self.env.ref("base.fr"), lang="en_US"
        )
        self.assertEqual(docset, self.docset2)

    def test_docset_no_match(self):
        docset = self.product1.get_usage_document_sets(
            "internal", self.env.ref("base.fr"), "en_FR"
        )
        self.assertFalse(docset)
