from odoo.tests.common import TransactionCase


class TestProductAttributeMultiCompany(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company1 = cls.env.ref("base.main_company")
        cls.company2 = cls.env["res.company"].create(
            {
                "name": "company 2",
                "parent_id": cls.env.ref("base.main_company").id,
            }
        )
        cls.user1 = cls.env.ref("base.user_admin")
        cls.user2 = cls.user1.copy(
            {
                "company_id": cls.company2.id,
                "company_ids": [(6, 0, [cls.company2.id])],
            }
        )

        cls.attribute = cls.env["product.attribute"]
        cls.attribute_value = cls.env["product.attribute.value"]

        cls.attribute_1 = cls.attribute.create(
            {
                "name": "attribute_1",
            }
        )
        cls.attribute_1_value_1 = cls.attribute_value.create(
            {
                "name": "attribute_1_value_1",
                "attribute_id": cls.attribute_1.id,
            }
        )

    ######################
    # Tests for attributes
    ######################

    def test_new_attribute_is_favorite_for_current_company(self):

        attribute_list1 = (
            self.env["product.attribute"]
            .with_user(self.user1.id)
            .search([("is_favorite", "=", True), ("id", "=", self.attribute_1.id)])
        )
        self.assertEqual(len(attribute_list1), 1)

    def test_new_attribute_is_not_favorite_for_other_company(self):

        attribute_list1 = (
            self.env["product.attribute"]
            .with_user(self.user2.id)
            .search([("is_favorite", "=", True), ("id", "=", self.attribute_1.id)])
        )
        self.assertEqual(len(attribute_list1), 0)

    def test_not_favorite_attribute_in_name_search_for_current_company(self):

        attribute_list1 = (
            self.env["product.attribute"]
            .with_user(self.user1.id)
            .name_search(name="attribute_1")
        )
        self.assertEqual(len(attribute_list1), 1)

    def test_not_favorite_attribute_not_in_name_search_for_other_company(self):

        attribute_list1 = (
            self.env["product.attribute"]
            .with_user(self.user2.id)
            .name_search(name="attribute_1")
        )
        self.assertEqual(len(attribute_list1), 0)

    def test_new_attribute_is_favorite_for_other_company_if_settings_all_company(self):
        """if the setting new_attribute_favorite_for_all_companies is True,
        a new attribute should be favorite for other companies"""

        self.env["ir.config_parameter"].sudo().set_param(
            "product_attribute_company_favorite.product_attribute_enable_for_all_companies",
            True,
        )
        self.attribute_2 = self.attribute.create(
            {
                "name": "attribute_2",
            }
        )
        attribute_list1 = (
            self.env["product.attribute"]
            .with_user(self.user2.id)
            .search([("is_favorite", "=", True), ("id", "=", self.attribute_2.id)])
        )
        self.assertEqual(len(attribute_list1), 1)

    ############################
    # Tests for attribute values
    ############################

    def test_new_attribute_value_is_favorite_for_current_company(self):

        attribute_value_list = (
            self.env["product.attribute.value"]
            .with_user(self.user1.id)
            .search(
                [("is_favorite", "=", True), ("id", "=", self.attribute_1_value_1.id)]
            )
        )
        self.assertEqual(len(attribute_value_list), 1)

    def test_new_attribute_value_is_not_favorite_for_other_company(self):

        attribute_value_list = (
            self.env["product.attribute.value"]
            .with_user(self.user2.id)
            .search(
                [("is_favorite", "=", True), ("id", "=", self.attribute_1_value_1.id)]
            )
        )
        self.assertEqual(len(attribute_value_list), 0)

    def test_not_favorite_attrib_value_not_in_name_search_for_current_company(self):

        attribute_value_list = (
            self.env["product.attribute.value"]
            .with_user(self.user1.id)
            .name_search(name="attribute_1")
        )
        self.assertEqual(len(attribute_value_list), 1)

    def test_not_favorite_attribute_value_not_in_name_search_for_other_company(self):

        attribute_value_list = (
            self.env["product.attribute.value"]
            .with_user(self.user2.id)
            .name_search(name="attribute_value_1")
        )
        self.assertEqual(len(attribute_value_list), 0)

    def test_new_attribute_is_favorite_value_for_other_company_if_settings_all_company(
        self,
    ):
        """if the setting new_attribute_values_favorite_for_all_companies is True,
        a new attribute value should be favorite for other companies"""

        self.env["ir.config_parameter"].sudo().set_param(
            "product_attribute_company_favorite."
            "product_attribute_value_enable_for_all_companies",
            True,
        )
        self.attribute_1_value_2 = self.attribute_value.create(
            {
                "name": "attribute_1_value_2",
                "attribute_id": self.attribute_1.id,
            }
        )
        attribute_value_list = (
            self.env["product.attribute.value"]
            .with_user(self.user2.id)
            .search(
                [("is_favorite", "=", True), ("id", "=", self.attribute_1_value_2.id)]
            )
        )
        self.assertEqual(len(attribute_value_list), 1)
