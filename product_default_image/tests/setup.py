# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64
from io import BytesIO
from PIL import Image

from odoo.tests.common import TransactionCase


class Setup(TransactionCase):

    def setUp(self):
        super(Setup, self).setUp()

        # Categ of tmpl_1
        self.categ_1 = self.env.ref(
            'product_default_image.demo_product_category_1'
        )
        self.tmpl_1 = self.env.ref(
            'product_default_image.demo_product_template_1'
        )

        # Categ of tmpl_2
        self.categ_2 = self.env.ref(
            'product_default_image.demo_product_category_2'
        )
        self.tmpl_2 = self.env.ref(
            'product_default_image.demo_product_template_2'
        )

        self.company_1 = self.env.ref(
            'product_default_image.demo_res_company_1'
        )

        self.env.user.company_id = self.company_1

        self.tmpl_1.company_id = self.company_1
        self.tmpl_2.company_id = self.company_1

        self.img_red = self.create_test_image(color=(256, 0, 0))
        self.img_green = self.create_test_image(color=(0, 256, 0))
        self.img_blue = self.create_test_image(color=(0, 0, 256))

        self.tmpl_mod = self.env['product.template']
        self.abs_mod = self.env['abstract.product.image']

    def create_test_image(self, color):
        # color arg should be (r, g, b)
        file_data = BytesIO()
        image = Image.new('RGBA', size=(4, 4), color=(color))
        image.save(file_data, 'png')
        file_data.name = 'test.png'
        file_data.seek(0)
        return base64.b64encode(file_data.read())
