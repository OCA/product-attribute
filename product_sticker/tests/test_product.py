from .common import ProductStickerCommon


class TestStickersOnProducts(ProductStickerCommon):
    def _test_model_availability(self, product):
        stickers = product.get_product_stickers()
        same_model = self.env.ref("base.model_ir_model")
        stickers.write({"available_model_ids": [(6, 0, same_model.ids)]})
        # Test same model
        self.assertEqual(
            len(
                product.get_product_stickers(
                    extra_domain=[
                        "|",
                        ("available_model_ids", "in", same_model.ids),
                        ("available_model_ids", "=", False),
                    ]
                )
            ),
            len(stickers),
            "Stickers must be present because has the same model",
        )
        # Test different model
        other_model = self.env.ref("base.model_ir_ui_view")
        self.assertEqual(
            len(
                product.get_product_stickers(
                    extra_domain=[
                        "|",
                        ("available_model_ids", "in", other_model.ids),
                        ("available_model_ids", "=", False),
                    ]
                )
            ),
            0,
            "Stickers must not be present because has different model",
        )

    def test_global_stickers(self):
        stickers = self.product_as500.product_variant_ids.get_product_stickers()
        self.assertEqual(len(stickers), 1, "Global sticker must be present")

    def test_product_product_stickers(self):
        stickers = self.product_as400.product_variant_ids[0].get_product_stickers()
        self.assertEqual(
            len(stickers), 2, "Attribute that create variants has been generated"
        )
        # Add a new attribute value to the template
        self.product_as400.attribute_line_ids.filtered(
            lambda al: al.attribute_id == self.att_license
        ).write(
            {
                "value_ids": [(4, self.att_license_freemium.id)],
            }
        )
        new_stickers = self.product_as400.product_variant_ids[0].get_product_stickers()
        self.assertEqual(
            len(new_stickers),
            3,
            "Sticker for Attribute with no create variants not present",
        )
        # Test models
        self._test_model_availability(self.product_as400.product_variant_ids[0])

    def test_image_sizes(self):
        stickers = self.product_as400.product_variant_ids.get_product_stickers()
        for sticker in stickers:
            with self.subTest(sticker=sticker):
                self.assertEqual(sticker.image_64, sticker.get_image())

        stickers.write({"image_size": "128"})
        for sticker in stickers:
            with self.subTest(sticker=sticker):
                self.assertEqual(sticker.image_128, sticker.get_image())
