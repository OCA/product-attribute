# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from .common import Common


class TestProductPackagingContainerDeposit(Common):
    def test_product_container_deposit_qties_with_not_set_container_deposit_on_packaging_type(
        self,
    ):
        self.package_type_pallet.container_deposit_product_id = False
        self.package_type_box.container_deposit_product_id = False
        packaging_qties = self.product_a.get_product_container_deposit_quantities(280)
        self.assertEqual(packaging_qties, {})

    def test_product_container_deposit_quantities_per_packaging_level(self):
        packaging_qties = self.product_a.get_product_container_deposit_quantities(280)
        self.assertEqual(
            packaging_qties,
            {
                self.product_packaging_level_pallet: (
                    self.package_type_pallet.container_deposit_product_id,
                    1,
                ),
                self.product_packaging_level_box: (
                    self.package_type_box.container_deposit_product_id,
                    11,
                ),
            },
        )

    def test_product_container_deposit_negative_quantity(self):
        packaging_qties = self.product_a.get_product_container_deposit_quantities(-280)
        self.assertEqual(
            packaging_qties,
            {
                self.product_packaging_level_box: (
                    self.package_type_box.container_deposit_product_id,
                    -11,
                ),
                self.product_packaging_level_pallet: (
                    self.package_type_pallet.container_deposit_product_id,
                    -1,
                ),
            },
        )
