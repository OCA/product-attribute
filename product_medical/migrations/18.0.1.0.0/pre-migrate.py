#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

MODEL_TO_RENAMED_FIELDS = {
    "product.template": [
        ("ppe_category_id", "medical_ppe_category_id"),
        ("in_vitro_diagnostic", "medical_in_vitro_diagnostic"),
        ("in_vitro_diagnostic", "medical_in_vitro_diagnostic"),
        ("conformity_declaration_ids", "medical_conformity_declaration_ids"),
        ("doc_lot_related", "medical_doc_lot_related"),
        ("doc_validity_date", "medical_doc_validity_date"),
        (
            "ce_certificate_medical_class_ids",
            "medical_ce_certificate_class_ids",
        ),
        ("ce_certificate_validity_date", "medical_ce_certificate_validity_date"),
        ("notified_body_id", "medical_notified_body_id"),
    ]
}


def _rename_fields(env):
    openupgrade.rename_fields(
        env,
        [
            (
                model_name,
                env[model_name]._table,
                field_spec[0],
                field_spec[1],
            )
            for model_name, field_specs in MODEL_TO_RENAMED_FIELDS.items()
            for field_spec in field_specs
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    _rename_fields(env)
