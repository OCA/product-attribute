# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase

from odoo.addons.attachment_zipped_download.tests.test_attachment_zipped_download import (
    TestAttachmentZippedDownloadBase,
)


class TestProductAttachmentZippedDownload(
    TransactionCase, TestAttachmentZippedDownloadBase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_a = cls.env["product.product"].create({"name": "Test product A"})
        cls.product_b = cls.env["product.product"].create({"name": "Test product B"})
        cls.product_c = cls.env["product.product"].create({"name": "Test product C"})
        cls.attachment_a = cls._create_attachment(
            cls.env,
            cls.env.uid,
            "product-a.txt",
            model=cls.product_a._name,
            res_id=cls.product_a.id,
        )
        cls.attachment_b = cls._create_attachment(
            cls.env,
            cls.env.uid,
            "product-b.txt",
            model=cls.product_b._name,
            res_id=cls.product_b.id,
        )
        cls.attachment_b_extra = cls._create_attachment(
            cls.env,
            cls.env.uid,
            "product-template-b.txt",
            model=cls.product_b.product_tmpl_id._name,
            res_id=cls.product_b.product_tmpl_id.id,
        )

    def test_action_download_attachments_no_attachment(self):
        action = self.product_c.product_tmpl_id.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.client")
        self.assertEqual(action["tag"], "display_notification")
        action = self.product_c.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.client")
        self.assertEqual(action["tag"], "display_notification")

    def test_action_download_attachments_one_attachment_1(self):
        action = self.product_a.product_tmpl_id.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertEqual(
            action["url"], "/web/content/%s?download=1" % self.attachment_a.id
        )
        action = self.product_a.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertEqual(
            action["url"], "/web/content/%s?download=1" % self.attachment_a.id
        )

    def test_action_download_attachments_one_attachment_2(self):
        action = self.product_b.product_tmpl_id.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        attachment_ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertNotIn(self.attachment_a.id, attachment_ids)
        self.assertIn(self.attachment_b.id, attachment_ids)
        self.assertIn(self.attachment_b_extra.id, attachment_ids)
        action = self.product_b.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        attachment_ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertNotIn(self.attachment_a.id, attachment_ids)
        self.assertIn(self.attachment_b.id, attachment_ids)
        self.assertIn(self.attachment_b_extra.id, attachment_ids)

    def test_action_download_attachments_multi_attachment(self):
        products = self.product_a + self.product_b + self.product_c
        product_templates = products.mapped("product_tmpl_id")
        action = product_templates.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        attachment_ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertIn(self.attachment_a.id, attachment_ids)
        self.assertIn(self.attachment_b.id, attachment_ids)
        self.assertIn(self.attachment_b_extra.id, attachment_ids)
        action = products.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        attachment_ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertIn(self.attachment_a.id, attachment_ids)
        self.assertIn(self.attachment_b.id, attachment_ids)
        self.assertIn(self.attachment_b_extra.id, attachment_ids)
