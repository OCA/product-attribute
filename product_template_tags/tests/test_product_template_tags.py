# Copyright 2018 Kolushov Alexandr
# Copyright 2018 <https://it-projects.info/team/KolushovAlexandr>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductTemplateTag(TransactionCase):
    pre_install = True
    post_install = True

    def test_products_count(self):
        tag = self.env['product.template.tag'].create({
            'name': 'test_tag',
        })
        product = self.env['product.template'].search([], limit=1)
        product.write({
            'tag_ids': [(6, 0, [tag.id])],
        })
        self.assertEqual(product.tag_ids[0].products_count,
                         1,
                         'Error product count does not match')
