# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _assign_profile_and_recompute(env):
    abc_profile = env["abc.classification.profile"].search([])
    env["product.product"].with_context(active_test=False).search([]).write(
        {"abc_classification_profile_id": abc_profile.id}
    )
    env["product.template"].with_context(active_test=False).search([]).write(
        {"abc_classification_profile_id": abc_profile.id}
    )
    abc_profile._compute_abc_classification()


@openupgrade.migrate()
def migrate(env, version):
    """To notice: abc_product_classification profile assignment to products isn't
    company dependant as product_sale_classification level fields were. So there's no
    way to ensure at this moment the proper profile in a multi-company environment.
    So we'll only consider the case for a single company scenario"""
    if len(env["res.company"].search([])) == 1:
        _assign_profile_and_recompute(env)
