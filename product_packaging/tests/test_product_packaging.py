# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
from odoo.addons.product.tests.common import ProductCommon
from odoo.addons.product_packaging.hooks import post_init_hook


class TestProductPackaging(ProductCommon):
    """Tests for the per-variant product.packaging model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        # 144 units, relative to the category reference (unit).
        cls.uom_gross = cls.env["uom.uom"].create(
            {
                "name": "Gross",
                "relative_factor": 144,
                "relative_uom_id": cls.uom_unit.id,
            }
        )
        cls.color_attribute = cls.env["product.attribute"].create(
            {
                "name": "Color",
                "value_ids": [
                    Command.create({"name": "Red"}),
                    Command.create({"name": "Blue"}),
                ],
            }
        )

    def _create_template_with_variants(self):
        """Template carrying the color attribute, hence two variants."""
        return self.env["product.template"].create(
            {
                "name": "Multi variant",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color_attribute.id,
                            "value_ids": [
                                Command.set(self.color_attribute.value_ids.ids)
                            ],
                        }
                    )
                ],
            }
        )

    def test_uom_ids_and_packaging_stay_consistent(self):
        """The template's UoM list and the variant's packagings mirror each other.

        Scenario:
            1. On a single-variant product, add a packaging UoM from the
               template side.
            2. Add another packaging UoM from the variant side.
            3. Remove the first UoM again from the template side.
        Expected:
            - Each change made on one side is immediately visible on the other;
              the template's UoM list and the variant's packagings always match.
        """
        product = self._create_product()
        template = product.product_tmpl_id

        # Linking a UoM on the template creates the variant's packaging.
        template.uom_ids = [Command.link(self.uom_dozen.id)]
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen)

        # Creating a packaging on the variant is reflected on uom_ids.
        product.packaging_ids = [Command.create({"uom_id": self.uom_pack_6.id})]
        self.assertIn(self.uom_pack_6, template.uom_ids)

        # Unlinking the UoM removes the matching packaging.
        with mute_logger("odoo.models.unlink"):
            template.write({"uom_ids": [Command.unlink(self.uom_dozen.id)]})
        self.assertEqual(product.packaging_ids.uom_id, self.uom_pack_6)

    def test_uom_ids_inverse_fans_out_to_all_variants(self):
        """Editing the template's UoM list updates every variant at once.

        Scenario:
            1. On a product with two variants, add a packaging UoM on the
               template.
            2. Remove that UoM again.
        Expected:
            - Adding the UoM creates the matching packaging on both variants.
            - Removing it deletes the packaging from both variants.
        """
        template = self._create_template_with_variants()
        self.assertEqual(len(template.product_variant_ids), 2)

        template.uom_ids = [Command.link(self.uom_dozen.id)]
        for variant in template.product_variant_ids:
            self.assertEqual(variant.packaging_ids.uom_id, self.uom_dozen)

        with mute_logger("odoo.models.unlink"):
            template.write({"uom_ids": [Command.unlink(self.uom_dozen.id)]})
        for variant in template.product_variant_ids:
            self.assertFalse(variant.packaging_ids)

    def test_uom_ids_wholesale_replace_from_template(self):
        """Replacing the whole UoM list on the template reconciles the packagings.

        Scenario:
            1. Give a product two packaging UoMs.
            2. Replace the whole UoM list with a single different UoM by writing
               on the template.
        Expected:
            - The two original packagings are removed and the new one is created.
        """
        product = self._create_product()
        template = product.product_tmpl_id

        template.uom_ids = [Command.set([self.uom_dozen.id, self.uom_pack_6.id])]
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen | self.uom_pack_6)

        with mute_logger("odoo.models.unlink"):
            template.uom_ids = [Command.set([self.uom_gross.id])]
        self.assertEqual(product.packaging_ids.uom_id, self.uom_gross)

    def test_uom_ids_wholesale_replace_from_variant(self):
        """Replacing the whole UoM list on the variant reconciles the packagings.

        Scenario:
            1. Give a product two packaging UoMs.
            2. Replace the whole UoM list with a single different UoM by writing
               on the variant.
        Expected:
            - The two original packagings are removed and the new one is created.
        """
        product = self._create_product()

        product.uom_ids = [Command.set([self.uom_dozen.id, self.uom_pack_6.id])]
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen | self.uom_pack_6)

        with mute_logger("odoo.models.unlink"):
            product.uom_ids = [Command.set([self.uom_gross.id])]
        self.assertEqual(product.packaging_ids.uom_id, self.uom_gross)

    def test_divergent_per_variant_packagings(self):
        """Variants may carry different packagings; the UoM list is their union.

        Scenario:
            1. On a two-variant product, add a packaging to one variant only
               (directly on that variant, not through the shared UoM list).
            2. Add the same packaging to the second variant too.
            3. Remove it again from the first variant only.
        Expected:
            - After step 1, only the first variant has the packaging, and the
              product's UoM list lists the UoM (the union of all variants).
            - After step 3, the first variant no longer has it, the second still
              does, and the UoM list still lists it (kept by the second variant).
        """
        template = self._create_template_with_variants()
        variant_a, variant_b = template.product_variant_ids

        # 1. Packaging on variant A only -> not fanned out to variant B.
        variant_a.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        self.assertEqual(variant_a.packaging_ids.uom_id, self.uom_dozen)
        self.assertFalse(variant_b.packaging_ids)
        self.assertEqual(template.uom_ids, self.uom_dozen)

        # 2. Same packaging on variant B too.
        variant_b.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]

        # 3. Remove it from variant A only.
        with mute_logger("odoo.models.unlink"):
            variant_a.packaging_ids.unlink()
        self.assertFalse(variant_a.packaging_ids)
        self.assertEqual(variant_b.packaging_ids.uom_id, self.uom_dozen)
        self.assertEqual(template.uom_ids, self.uom_dozen)

    def test_barcode_packaging_consistency_is_enforced(self):
        """A barcode cannot point to a packaging with a different UoM.

        Scenario:
            1. On a product with a "dozen" and a "pack of 6" packaging, create a
               barcode for the dozen UoM.
            2. Force that barcode to point to the pack-of-6 packaging instead.
        Expected:
            - The inconsistency is rejected with a validation error.
        """
        product = self._create_product()
        product.packaging_ids = [
            Command.create({"uom_id": self.uom_dozen.id}),
            Command.create({"uom_id": self.uom_pack_6.id}),
        ]
        pkg_pack6 = product.packaging_ids.filtered(
            lambda p: p.uom_id == self.uom_pack_6
        )
        barcode = self.env["product.uom"].create(
            {
                "product_id": product.id,
                "uom_id": self.uom_dozen.id,
                "barcode": "9999999999999",
            }
        )
        with self.assertRaisesRegex(ValidationError, "packaging UoM must match"):
            barcode.packaging_id = pkg_pack6
            self.env.flush_all()

    def test_new_variant_inherits_packaging(self):
        """New variants inherit the packagings already defined on the product.

        Scenario:
            1. Start from a product that already has a packaging UoM.
            2. Add an attribute that turns it into a two-variant product.
        Expected:
            - Both freshly created variants automatically get the packaging that
              was already defined on the product.
        """
        template = self.env["product.template"].create(
            {
                "name": "Grows variants",
                "uom_id": self.uom_unit.id,
                "uom_ids": [Command.link(self.uom_dozen.id)],
            }
        )
        self.assertEqual(
            template.product_variant_ids.packaging_ids.uom_id, self.uom_dozen
        )

        # Adding an attribute line spawns new variants.
        template.attribute_line_ids = [
            Command.create(
                {
                    "attribute_id": self.color_attribute.id,
                    "value_ids": [Command.set(self.color_attribute.value_ids.ids)],
                }
            )
        ]
        self.assertEqual(len(template.product_variant_ids), 2)
        for variant in template.product_variant_ids:
            self.assertEqual(variant.packaging_ids.uom_id, self.uom_dozen)

    def test_create_template_with_attributes_and_uom_ids(self):
        """Creating a multi-variant product with UoMs packages every variant.

        Scenario:
            1. Create a product in a single step with both an attribute (two
               variants) and two packaging UoMs.
        Expected:
            - Two variants are created.
            - The product's UoM list shows both UoMs.
            - Each variant gets a packaging for each of the two UoMs.
        """
        template = self.env["product.template"].create(
            {
                "name": "Attrs and uoms",
                "uom_id": self.uom_unit.id,
                "uom_ids": [Command.set([self.uom_dozen.id, self.uom_pack_6.id])],
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color_attribute.id,
                            "value_ids": [
                                Command.set(self.color_attribute.value_ids.ids)
                            ],
                        }
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 2)
        self.assertEqual(template.uom_ids, self.uom_dozen | self.uom_pack_6)
        for variant in template.product_variant_ids:
            self.assertEqual(
                variant.packaging_ids.uom_id, self.uom_dozen | self.uom_pack_6
            )

    def test_create_template_with_attributes_without_uom_ids(self):
        """Creating a multi-variant product without UoMs creates no packaging.

        Scenario:
            1. Create a product with an attribute (two variants) but no
               packaging UoMs.
        Expected:
            - Two variants are created.
            - Neither the product's UoM list nor the variants have any packaging.
        """
        template = self._create_template_with_variants()
        self.assertEqual(len(template.product_variant_ids), 2)
        self.assertFalse(template.uom_ids)
        self.assertFalse(template.product_variant_ids.packaging_ids)

    def test_create_product_with_uom_ids(self):
        """Creating a variant directly with UoMs packages it and syncs the list.

        Scenario:
            1. Create a ``product.product`` directly (not through its template)
               with one packaging UoM.
        Expected:
            - The variant gets the matching packaging.
            - The product's UoM list reflects that UoM.
        """
        product = self.env["product.product"].create(
            {
                "name": "Product with uoms",
                "uom_id": self.uom_unit.id,
                "uom_ids": [Command.link(self.uom_dozen.id)],
            }
        )
        self.assertEqual(product.product_tmpl_id.uom_ids, self.uom_dozen)
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen)

    def test_create_product_with_packaging_ids(self):
        """Creating a variant with packagings fills in the UoM list from them.

        Scenario:
            1. Create a ``product.product`` directly with a packaging (giving
               only the packaging, not the UoM list).
        Expected:
            - The packaging is kept.
            - The product's UoM list is derived to include that packaging's UoM.
        """
        product = self.env["product.product"].create(
            {
                "name": "Product with packagings",
                "uom_id": self.uom_unit.id,
                "packaging_ids": [Command.create({"uom_id": self.uom_dozen.id})],
            }
        )
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen)
        self.assertEqual(product.product_tmpl_id.uom_ids, self.uom_dozen)

    def test_create_template_with_packaging_ids_single_variant(self):
        """Creating a product with packagings fills in the UoM list from them.

        Scenario:
            1. Create a single-variant product through its template, providing
               a packaging (and no UoM list).
        Expected:
            - The single variant keeps the packaging.
            - The product's UoM list is derived to include that packaging's UoM.
        """
        template = self.env["product.template"].create(
            {
                "name": "Template with packagings",
                "uom_id": self.uom_unit.id,
                "packaging_ids": [Command.create({"uom_id": self.uom_dozen.id})],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 1)
        self.assertEqual(
            template.product_variant_ids.packaging_ids.uom_id, self.uom_dozen
        )
        self.assertEqual(template.uom_ids, self.uom_dozen)

    def test_qty_factor(self):
        """The packaging quantity equals how many base units it contains.

        Scenario:
            1. Add a "dozen" packaging to a product sold in units.
            2. Add a "gross" (144 units) packaging to a product sold in dozens.
        Expected:
            - The dozen packaging reports a quantity of 12 base units.
            - The gross packaging reports 12 (144 units ÷ 12 units per dozen).
        """
        # Base UoM is the category reference (unit).
        product = self._create_product()
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        self.assertEqual(product.packaging_ids.qty, 12)

        # Base UoM is NOT the reference (dozen): 144 units / 12 = 12 dozens.
        product_dozen = self._create_product(uom_id=self.uom_dozen.id)
        product_dozen.packaging_ids = [Command.create({"uom_id": self.uom_gross.id})]
        self.assertEqual(product_dozen.packaging_ids.qty, 12)

    def test_weight_and_volume_seeded_then_preserved(self):
        """Packaging weight/volume start from the product but stay user-editable.

        Scenario:
            1. Add a dozen packaging to a product weighing 2 (volume 3).
            2. Manually override the packaging weight to 50.
            3. Make an unrelated edit on the packaging.
        Expected:
            - The packaging is initially seeded to 24 weight / 36 volume
              (per-unit value × 12).
            - The manual weight override of 50 survives the unrelated edit (it
              is not recomputed away).
        """
        product = self._create_product(weight=2.0, volume=3.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.weight, 24.0)  # 2.0 * 12
        self.assertEqual(packaging.volume, 36.0)  # 3.0 * 12

        # A manual override survives an unrelated write (no recompute on product_id).
        packaging.weight = 50.0
        packaging.sequence = 5
        self.assertEqual(packaging.weight, 50.0)

    def test_weight_and_volume_kept_on_product_change(self):
        """Changing the product's weight/volume leaves its packagings untouched.

        Scenario:
            1. Add a dozen packaging to a product weighing 2 (volume 3).
            2. Change the product's weight and volume.
        Expected:
            - The packaging keeps the values it was seeded with, rather than
              having a possibly user-defined value overwritten.
        """
        product = self._create_product(weight=2.0, volume=3.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.weight, 24.0)  # 2.0 * 12
        self.assertEqual(packaging.volume, 36.0)  # 3.0 * 12

        product.write({"weight": 5.0, "volume": 7.0})
        self.assertEqual(packaging.weight, 24.0)
        self.assertEqual(packaging.volume, 36.0)

    def test_set_packaging_weight_via_template(self):
        """A weight set on a packaging through the template form is saved.

        Scenario:
            1. On a single-variant product with no weight, create a packaging
               and set its weight, editing through the template (as the form
               does).
            2. Then change that existing packaging's weight, again through the
               template.
        Expected:
            - The weight is saved both when set on creation and when updated
              later (it is not reset to 0).
        """
        product = self._create_product()  # weight 0
        template = product.product_tmpl_id

        template.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id, "weight": 5.0})
        ]
        packaging = template.packaging_ids
        self.assertEqual(packaging.weight, 5.0)

        # The form sends an update command on the (computed) packaging_ids field.
        template.packaging_ids = [Command.update(packaging.id, {"weight": 8.0})]
        self.assertEqual(packaging.weight, 8.0)

    def test_set_packaging_weight_via_variant(self):
        """A weight set on a packaging through the variant form is saved.

        Scenario:
            1. On a product with no weight, create a packaging through the
               variant and set its weight.
            2. Update that weight again through the variant.
        Expected:
            - The weight is saved on creation and on update (not reset to 0).
            - The same value is seen when reading the packaging from the
              template (single-variant mirror).
        """
        product = self._create_product()  # weight 0
        template = product.product_tmpl_id

        product.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id, "weight": 5.0})
        ]
        packaging = product.packaging_ids
        self.assertEqual(packaging.weight, 5.0)
        self.assertEqual(template.packaging_ids.weight, 5.0)

        product.packaging_ids = [Command.update(packaging.id, {"weight": 8.0})]
        self.assertEqual(packaging.weight, 8.0)
        self.assertEqual(template.packaging_ids.weight, 8.0)

    def test_set_packaging_volume_via_template(self):
        """A volume set on a packaging through the template form is saved.

        Scenario:
            1. On a single-variant product with no volume, create a packaging
               through the template and set its volume.
            2. Update that volume again through the template.
        Expected:
            - The volume is saved on creation and on update (not reset to 0).
        """
        product = self._create_product()  # volume 0
        template = product.product_tmpl_id

        template.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id, "volume": 3.0})
        ]
        packaging = template.packaging_ids
        self.assertEqual(packaging.volume, 3.0)

        template.packaging_ids = [Command.update(packaging.id, {"volume": 7.0})]
        self.assertEqual(packaging.volume, 7.0)

    def test_set_weights_on_multiple_packagings_via_template(self):
        """Weights set on several packagings in one save are all kept.

        Scenario:
            1. On a single-variant product, create two packagings (pack of 6 and
               dozen) through the template.
            2. In a single template write, set a distinct weight on each.
        Expected:
            - Both weights are saved (neither is reset to 0).
        """
        product = self._create_product()
        template = product.product_tmpl_id
        template.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id}),
            Command.create({"uom_id": self.uom_dozen.id}),
        ]
        pkg_6 = template.packaging_ids.filtered(lambda p: p.uom_id == self.uom_pack_6)
        pkg_12 = template.packaging_ids.filtered(lambda p: p.uom_id == self.uom_dozen)

        template.packaging_ids = [
            Command.update(pkg_6.id, {"weight": 6.0}),
            Command.update(pkg_12.id, {"weight": 12.0}),
        ]
        self.assertEqual(pkg_6.weight, 6.0)
        self.assertEqual(pkg_12.weight, 12.0)

    def test_create_and_update_packagings_in_one_template_write(self):
        """A single save that edits one packaging and adds another keeps both.

        Scenario:
            1. On a single-variant product, create a packaging through the
               template.
            2. In a single template write, update that packaging's weight and
               create a second packaging with its own weight.
        Expected:
            - The updated weight and the new packaging's weight are both saved.
        """
        product = self._create_product()
        template = product.product_tmpl_id
        template.packaging_ids = [Command.create({"uom_id": self.uom_pack_6.id})]
        pkg_6 = template.packaging_ids

        template.packaging_ids = [
            Command.update(pkg_6.id, {"weight": 6.0}),
            Command.create({"uom_id": self.uom_dozen.id, "weight": 12.0}),
        ]
        self.assertEqual(pkg_6.weight, 6.0)
        pkg_12 = template.packaging_ids.filtered(lambda p: p.uom_id == self.uom_dozen)
        self.assertEqual(pkg_12.weight, 12.0)

    def test_reorder_packagings_via_template(self):
        """Reordering packagings through the template form is saved.

        Scenario:
            1. On a single-variant product, create two packagings through the
               template.
            2. Swap their sequence in a single template write (as the handle
               widget does).
        Expected:
            - The new sequence values are saved.
        """
        product = self._create_product()
        template = product.product_tmpl_id
        template.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id, "sequence": 1}),
            Command.create({"uom_id": self.uom_dozen.id, "sequence": 2}),
        ]
        pkg_6 = template.packaging_ids.filtered(lambda p: p.uom_id == self.uom_pack_6)
        pkg_12 = template.packaging_ids.filtered(lambda p: p.uom_id == self.uom_dozen)

        template.packaging_ids = [
            Command.update(pkg_6.id, {"sequence": 2}),
            Command.update(pkg_12.id, {"sequence": 1}),
        ]
        self.assertEqual(pkg_6.sequence, 2)
        self.assertEqual(pkg_12.sequence, 1)

    def test_add_barcode_to_packaging_via_template(self):
        """A barcode added to a packaging through the template form is saved.

        Scenario:
            1. On a single-variant product, create a packaging through the
               template.
            2. Add a barcode to it through the template (a nested command on the
               packaging's barcodes).
        Expected:
            - The barcode is saved and linked to the right packaging.
        """
        product = self._create_product()
        template = product.product_tmpl_id
        template.packaging_ids = [Command.create({"uom_id": self.uom_pack_6.id})]
        packaging = template.packaging_ids

        template.packaging_ids = [
            Command.update(
                packaging.id,
                {"barcode_ids": [Command.create({"barcode": "1234567890123"})]},
            )
        ]
        self.assertEqual(packaging.barcode_ids.barcode, "1234567890123")
        self.assertEqual(packaging.barcode_ids.product_id, product)

    def test_weight_and_volume_reseed_on_uom_change(self):
        """Changing a packaging's UoM recomputes its weight and volume.

        Scenario:
            1. Add a dozen packaging to a product weighing 2 (volume 3).
            2. Change that packaging's UoM to a pack of 6.
        Expected:
            - The quantity drops from 12 to 6.
            - Weight is re-seeded to 12 and volume to 18.
        """
        product = self._create_product(weight=2.0, volume=3.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.weight, 24.0)  # 2.0 * 12

        packaging.uom_id = self.uom_pack_6  # qty 6
        self.assertEqual(packaging.qty, 6)
        self.assertEqual(packaging.weight, 12.0)  # 2.0 * 6
        self.assertEqual(packaging.volume, 18.0)  # 3.0 * 6

    def test_delete_variant_cascades_packaging(self):
        """Deleting a variant removes only its own packagings.

        Scenario:
            1. On a two-variant product that has a shared packaging UoM, delete
               one of the variants.
        Expected:
            - The deleted variant's packaging is gone.
            - The surviving variant keeps its packaging.
            - The product's UoM list still shows the UoM.
        """
        template = self._create_template_with_variants()
        template.uom_ids = [Command.link(self.uom_dozen.id)]
        variant_a, variant_b = template.product_variant_ids
        packaging_a = variant_a.packaging_ids

        with mute_logger("odoo.models.unlink"):
            variant_a.unlink()
        self.assertFalse(packaging_a.exists())
        self.assertTrue(variant_b.packaging_ids)
        self.assertEqual(template.uom_ids, self.uom_dozen)

    def test_qty_smaller_packaging_than_non_reference_base(self):
        """A packaging smaller than the base unit yields a fractional quantity.

        Scenario:
            1. On a product sold in dozens, add a "pack of 6" packaging, which
               is smaller than one dozen.
        Expected:
            - The packaging quantity is the fraction 0.5 (half a dozen).
        """
        # Base = dozen (12 units), packaging = pack of 6 (6 units) -> 0.5 dozen.
        product = self._create_product(uom_id=self.uom_dozen.id)
        product.packaging_ids = [Command.create({"uom_id": self.uom_pack_6.id})]
        self.assertEqual(product.packaging_ids.qty, 0.5)

    def test_weight_and_volume_scale_with_non_reference_base(self):
        """Weight/volume scale by quantity even when the base is not the reference.

        Scenario:
            1. On a product sold in dozens (weight 24, volume 6 per dozen), add
               a "gross" packaging, which holds 12 dozens.
        Expected:
            - The packaging weighs 288 (24 × 12).
            - The packaging volume is 72 (6 × 12).
        """
        # Base = dozen; values are per dozen. Packaging = gross -> qty 12 dozens.
        product = self._create_product(
            uom_id=self.uom_dozen.id, weight=24.0, volume=6.0
        )
        product.packaging_ids = [Command.create({"uom_id": self.uom_gross.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.qty, 12)
        self.assertEqual(packaging.weight, 288.0)  # 24.0 * 12
        self.assertEqual(packaging.volume, 72.0)  # 6.0 * 12

    def test_multiple_packagings_with_distinct_factors(self):
        """Each packaging on a product computes its own quantity independently.

        Scenario:
            1. On a product sold in units, add three packagings at once: a pack
               of 6, a dozen, and a gross.
        Expected:
            - Each packaging reports its own base-unit quantity: 6, 12 and 144.
        """
        product = self._create_product()  # base = unit (the reference)
        product.packaging_ids = [
            Command.create({"uom_id": self.uom_pack_6.id}),
            Command.create({"uom_id": self.uom_dozen.id}),
            Command.create({"uom_id": self.uom_gross.id}),
        ]
        qty_by_uom = {p.uom_id: p.qty for p in product.packaging_ids}
        self.assertEqual(qty_by_uom[self.uom_pack_6], 6)
        self.assertEqual(qty_by_uom[self.uom_dozen], 12)
        self.assertEqual(qty_by_uom[self.uom_gross], 144)

    def test_create_with_uom_ids_on_non_reference_base(self):
        """Packagings materialize correctly for a non-reference base UoM on create.

        Scenario:
            1. Create a product sold in dozens directly with a "gross"
               packaging UoM in its UoM list.
        Expected:
            - The gross packaging is created and reports a quantity of 12 dozens
              (144 units ÷ 12).
        """
        product = self.env["product.product"].create(
            {
                "name": "Non-reference base",
                "uom_id": self.uom_dozen.id,
                "uom_ids": [Command.link(self.uom_gross.id)],
            }
        )
        self.assertEqual(product.packaging_ids.uom_id, self.uom_gross)
        self.assertEqual(product.packaging_ids.qty, 12)  # 144 units / 12

    def test_barcodes_scoped_to_variant(self):
        """A barcode belongs to one variant's packaging only.

        Scenario:
            1. On a two-variant product sharing a packaging UoM, give each
               variant its own barcode.
            2. Delete one variant's packaging.
        Expected:
            - Each barcode links to its own variant's packaging.
            - Deleting one variant's packaging removes only that variant's
              barcode and leaves the other variant's barcode untouched.
        """
        template = self._create_template_with_variants()
        template.uom_ids = [Command.link(self.uom_dozen.id)]
        variant_a, variant_b = template.product_variant_ids

        barcode_a, barcode_b = self.env["product.uom"].create(
            [
                {
                    "uom_id": self.uom_dozen.id,
                    "product_id": variant_a.id,
                    "barcode": "1111111111111",
                },
                {
                    "uom_id": self.uom_dozen.id,
                    "product_id": variant_b.id,
                    "barcode": "2222222222222",
                },
            ]
        )
        # Each barcode is linked to its packaging, which exposes it.
        self.assertEqual(barcode_a.packaging_id, variant_a.packaging_ids)
        self.assertEqual(variant_a.packaging_ids.barcode_ids, barcode_a)

        # Removing variant A's packaging only drops variant A's barcode.
        with mute_logger("odoo.models.unlink"):
            variant_a.packaging_ids.unlink()
        self.assertFalse(barcode_a.exists())
        self.assertTrue(barcode_b.exists())

    def test_create_barcode_through_packaging(self):
        """A barcode added on a packaging inherits its product and UoM.

        Scenario:
            1. On a product with a dozen packaging, add a barcode directly
               through that packaging, giving only the barcode value.
        Expected:
            - The barcode is automatically linked to the right product, UoM and
              packaging without having to provide them.
        """
        product = self._create_product()
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids

        packaging.barcode_ids = [Command.create({"barcode": "1234567890123"})]
        barcode = packaging.barcode_ids
        self.assertEqual(barcode.product_id, product)
        self.assertEqual(barcode.uom_id, self.uom_dozen)
        self.assertEqual(barcode.packaging_id, packaging)

    def test_multiple_barcodes_per_packaging(self):
        """A packaging can carry several barcodes, and removing it drops them all.

        Scenario:
            1. Add two barcodes to a single packaging.
            2. Delete that packaging.
        Expected:
            - Both barcodes coexist on the packaging.
            - Deleting the packaging cascades away both barcodes.
        """
        product = self._create_product()
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        packaging.barcode_ids = [
            Command.create({"barcode": "1111111111111"}),
            Command.create({"barcode": "2222222222222"}),
        ]
        barcodes = packaging.barcode_ids
        self.assertEqual(len(barcodes), 2)
        with mute_logger("odoo.models.unlink"):
            packaging.unlink()
        self.assertFalse(barcodes.exists())

    def test_post_init_hook_backfills_packagings(self):
        """Installing the module creates packagings for pre-existing UoM data.

        Scenario:
            1. Simulate legacy data where a product already lists a UoM (a raw
               relation row) but has no packaging behind it.
            2. Run the module's post-install hook.
        Expected:
            - The hook backfills the missing packaging so the product ends up
              with a packaging for its existing UoM.
        """
        product = self._create_product()
        template = product.product_tmpl_id
        # Simulate legacy data: a uom_ids link with no packaging behind it.
        self.env.cr.execute(
            "INSERT INTO product_template_uom_uom_rel "
            "(product_template_id, uom_uom_id) VALUES (%s, %s)",
            (template.id, self.uom_dozen.id),
        )
        template.invalidate_recordset(["uom_ids"])
        self.assertFalse(product.packaging_ids)

        post_init_hook(self.env)
        self.assertEqual(product.packaging_ids.uom_id, self.uom_dozen)
