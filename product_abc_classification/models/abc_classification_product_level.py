# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AbcClassificationProductLevel(models.Model):
    _name = "abc.classification.product.level"
    _inherit = "mail.thread"
    _description = "Abc Classification Product Level"
    _rec_name = "level_id"

    display_name = fields.Char(compute="_compute_display_name")

    manual_level_id = fields.Many2one(
        "abc.classification.level",
        string="Manual classification level",
        tracking=True,
        domain="[('profile_id', '=', profile_id)]",
    )
    computed_level_id = fields.Many2one(
        "abc.classification.level",
        string="Computed classification level",
        readonly=True,
    )
    level_id = fields.Many2one(
        "abc.classification.level",
        string="Classification level",
        compute="_compute_level_id",
        store=True,
        domain="[('profile_id', '=', profile_id)]",
    )
    flag = fields.Boolean(
        default=False,
        compute="_compute_flag",
        string="If True, this means that the manual classification is "
        "different from the computed one",
        store=True,
        index=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        index=True,
        required=True,
        ondelete="cascade",
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product template",
        index=True,
        readonly=True,
    )
    # percentage
    profile_id = fields.Many2one(
        "abc.classification.profile",
        string="Profile",
        required=True,
    )
    profile_type = fields.Selection(
        related="profile_id.profile_type",
        readonly=True,
        store=True,
    )
    allowed_profile_ids = fields.Many2many(
        comodel_name="abc.classification.profile",
        related="product_id.abc_classification_profile_ids",
    )

    _sql_constraints = [
        (
            "product_level_uniq",
            "UNIQUE(profile_id, product_id)",
            _("Only one level by profile by product allowed"),
        )
    ]

    @api.constrains("computed_level_id", "manual_level_id", "product_id")
    def _check_level(self):
        for rec in self:
            if not rec.computed_level_id and not rec.manual_level_id:
                raise ValidationError(_("Classification level is mandatory"))
            if (
                rec.computed_level_id
                and rec.computed_level_id.profile_id != rec.profile_id
            ):
                raise ValidationError(
                    _(
                        "Computed level must be in  the same classifiation "
                        "profile as the one on the product level"
                    )
                )
            if rec.manual_level_id and rec.manual_level_id.profile_id != rec.profile_id:
                raise ValidationError(
                    _(
                        "Manual level must be in  the same classifiation "
                        "profile as the one on the product level"
                    )
                )

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        for rec in self.filtered(
            lambda a: a.product_tmpl_id.product_variant_count == 1
        ):
            rec.product_id = rec.product_tmpl_id.product_variant_id

    @api.depends("level_id", "profile_id")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "{profile_name}: {level_name}".format(
                profile_name=record.profile_id.name,
                level_name=record.level_id.name,
            )

    @api.depends("manual_level_id", "computed_level_id")
    def _compute_level_id(self):
        for rec in self:
            if rec.manual_level_id:
                rec.level_id = rec.manual_level_id
            else:
                rec.level_id = rec.computed_level_id

    @api.depends("manual_level_id", "computed_level_id")
    def _compute_flag(self):
        for rec in self:
            rec.flag = (
                rec.computed_level_id and rec.manual_level_id != rec.computed_level_id
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "manual_level_id" not in vals and "computed_level_id" in vals:
                # at creation the manual level is set to the same value as the
                # computed one
                vals["manual_level_id"] = vals["computed_level_id"]

            if "profile_id" in vals:
                profile = self.env["abc.classification.profile"].browse(
                    vals["profile_id"]
                )
                if profile.auto_apply_computed_value and "computed_level_id" in vals:
                    vals["manual_level_id"] = vals["computed_level_id"]
        return super().create(vals_list)

    def write(self, vals):
        """
        We apply the manual level to the product level if
        computed level is modified and only for profiles with
        auto_apply_computed_value = =True
        """
        values = vals.copy()
        new_self = self
        if "computed_level_id" in values:
            profile_obj = self.env["abc.classification.profile"]
            target_profile_id = (
                profile_obj.browse(values["profile_id"]).filtered(
                    "auto_apply_computed_value"
                )
                if "profile_id" in values
                else profile_obj.browse()
            )
            if target_profile_id:
                # If the profile of levels should be changed at the same time
                # and has auto_apply_computed_value True
                # So, we can apply change to the whole recordset
                values["manual_level_id"] = values["computed_level_id"]
            else:
                # If profile is not modified, filter levels per profile
                # if it has auto_apply_computed_value True and modify only
                # those ones
                auto_applied_profiles_levels = self.filtered(
                    lambda l: l.profile_id.auto_apply_computed_value
                )
                new_self = self - auto_applied_profiles_levels
                super(
                    AbcClassificationProductLevel, auto_applied_profiles_levels
                ).write(dict(values, manual_level_id=values["computed_level_id"]))
        return super(AbcClassificationProductLevel, new_self).write(values)
