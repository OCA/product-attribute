# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo_test_helper import FakeModelLoader

from odoo.tests import SavepointCase


class TestRatingMixin(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_model import FakeModel

        cls.loader.update_registry((FakeModel,))

        cls.test_model = cls.env[FakeModel._name].create({"name": "test"})
        cls.partner = cls.env.ref("base.res_partner_2")

        params = {
            "rating": 5,
            "feedback": "test",
            "res_id": cls.test_model.id,
            "res_model_id": cls.env.ref("rating_moderation.model_fake_model").id,
            "partner_id": cls.partner.id,
            "consumed": True,
        }
        cls.record = cls.env["rating.rating"].create(params)

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDown(cls)

    def test_compute_rating_avg(self):
        self.assertEqual(
            self.test_model.avg_rating, self.test_model.rating_get_stats()["avg"]
        )

    def test_domain(self):
        domain = self.test_model.action_view_reviews()["domain"]
        self.assertIn(self.test_model.id, domain[0][2])
        self.assertEqual(self.test_model._name, domain[1][2])
