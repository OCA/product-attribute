# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AbcClassificationProfile(models.Model):

    _name = "abc.classification.profile"
    _description = "Abc Classification Profile"
    _rec_name = "name"

    name = fields.Char(required=True)
    level_ids = fields.One2many(
        comodel_name="abc.classification.level", inverse_name="profile_id"
    )
    profile_type = fields.Selection(
        selection=[],
        string="Type of ABC classification",
        index=True,
        required=True,
    )
    period = fields.Integer(
        default=365,
        string="Period on which to compute the classification (Days)",
        required=True,
    )

    product_variant_ids = fields.Many2many(
        comodel_name="product.product",
        relation="abc_classification_profile_product_rel",
        column1="profile_id",
        column2="product_id",
        index=True,
    )
    product_count = fields.Integer(compute="_compute_product_count", readonly=True)

    auto_apply_computed_value = fields.Boolean(
        default=False,
        help="Check this if you want to apply the computed level on each product that has this "
        "profile.",
    )

    _sql_constraints = [("name_uniq", "UNIQUE(name)", _("Profile name must be unique"))]

    @api.constrains("level_ids")
    def _check_levels(self):
        for profile in self:
            percentages = profile.level_ids.mapped("percentage")
            total = sum(percentages)
            if profile.level_ids and total != 100.0:
                raise ValidationError(
                    _("The sum of the percentages of the levels should be " "100.")
                )
            if profile.level_ids and len({}.fromkeys(percentages)) != len(percentages):
                raise ValidationError(
                    _("The percentages of the levels must be unique.")
                )
            percentage_productss = profile.level_ids.mapped("percentage_products")
            total = sum(percentage_productss)
            if profile.level_ids and total != 100.0:
                raise ValidationError(
                    _(
                        "The sum of the products percentages of the levels "
                        "should be 100."
                    )
                )

    def _compute_abc_classification(self):
        raise NotImplementedError()

    @api.depends("product_variant_ids")
    def _compute_product_count(self):
        for profile in self:
            profile.product_count = len(profile.product_variant_ids)

    def action_view_products(self):
        products = self.mapped("product_variant_ids")
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product.product_variant_action"
        )
        del action["context"]
        if len(products) > 1:
            action["domain"] = [("id", "in", products.ids)]
        elif len(products) == 1:
            form_view = [
                (self.env.ref("product.product_variant_easy_edit_view").id, "form")
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = products.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    @api.model
    def _cron_compute_abc_classification(self):
        self.search([])._compute_abc_classification()

    def write(self, vals):
        res = super(AbcClassificationProfile, self).write(vals)
        if "auto_apply_computed_value" in vals and vals["auto_apply_computed_value"]:
            self._auto_apply_computed_value_for_product_levels()
        return res

    def _auto_apply_computed_value_for_product_levels(self):
        level_ids = []
        for rec in self:
            self.env.cr.execute(
                """
                    UPDATE %(table)s
                        SET manual_level_id = computed_level_id
                        WHERE profile_id = %(profile_id)s
                        RETURNING id

            """,
                {
                    "table": AsIs(self.env["abc.classification.product.level"]._table),
                    "profile_id": rec.id,
                },
            )
            level_ids.extend(r[0] for r in self.env.cr.fetchall())
        self.env["abc.classification.product.level"].invalidate_cache(
            ["manual_level_id"], level_ids
        )
        modified_levels = self.env["abc.classification.product.level"].browse(level_ids)
        # mark field as modified and trigger recompute of dependent fields.
        modified_levels.modified(["manual_level_id"])
        modified_levels._recompute_recordset()
