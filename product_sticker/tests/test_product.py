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

    def test_product_one_attribute(self):
        """Test that a product with only one attribute and one value that
        creates variants can have a sticker.

        Having only one value will not create variants with attribute values."""
        new_sticker = self.ps_att_cc.copy()
        new_sticker.write(
            {
                "name": "New Attribute",
                "product_attribute_id": self.att_platform.id,
                "product_attribute_value_id": self.att_platform_linux.id,
            }
        )
        # Create a product with only one attribute
        product = self.env["product.template"].create(
            {
                "name": "Single Attribute Product Create Variants",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.att_platform.id,
                            "value_ids": [(6, 0, [self.att_platform_linux.id])],
                        },
                    )
                ],
            }
        )
        stickers = product.product_variant_ids.get_product_stickers()
        self.assertIn(new_sticker, stickers, "New sticker must be present")
