# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from copy import deepcopy

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError

PROFILE_MENU = _(
    "Sales > Configuration \n> Product Categories and Attributes" "\n> Product Profiles"
)
# Prefix name of profile fields setting a default value,
# not an immutable value according to profile
PROF_DEFAULT_STR = "profile_default_"
LEN_DEF_STR = len(PROF_DEFAULT_STR)

_logger = logging.getLogger(__name__)


def format_except_message(error, field, self):
    value = self.profile_id[field]
    model = type(self)._name
    message = _(
        "Issue\n------\n"
        "%s\n'%s' value can't be applied to '%s' field."
        "\nThere is no matching value between 'Product Profiles' "
        "\nand '%s' models for this field.\n\n"
        "Resolution\n----------\n"
        "Check your settings on Profile model:\n%s"
        % (error, value, field, model, PROFILE_MENU)
    )
    return message


def get_profile_fields_to_exclude():
    # These fields must not be synchronized between product.profile
    # and product.template/product
    return models.MAGIC_COLUMNS + [
        "name",
        "explanation",
        "sequence",
        "id",
        "display_name",
        "__last_update",
    ]


class ProductProfile(models.Model):
    _name = "product.profile"
    _order = "sequence, name"
    _description = "Product Profile"

    name = fields.Char(
        required=True,
        help="Profile name displayed on product template\n"
        "(not synchronized with product.template fields)",
    )
    sequence = fields.Integer(
        help="Defines the order of the entries of profile_id field\n"
        "(not synchronized with product.template fields)"
    )
    explanation = fields.Text(
        required=True,
        help="An explanation on the selected profile\n"
        "(not synchronized with product.template fields)",
    )
    type = fields.Selection(
        selection=[("consu", "Consumable"), ("service", "Service")],
        required=True,
        default="consu",
        help="See 'type' field in product.template",
    )

    def write(self, vals):
        """Profile update can impact products: we take care to propagate
        ad hoc changes. If on the profile at least one field has changed,
        re-apply its values on relevant products"""
        excludable_fields = get_profile_fields_to_exclude()
        values_to_keep = deepcopy(vals)
        for key in vals:
            discard_value = (
                key.startswith(PROF_DEFAULT_STR)
                or key in excludable_fields
                or self.check_useless_key_in_vals(vals, key)
            )
            if discard_value:
                values_to_keep.pop(key)
        if values_to_keep:
            self._refresh_products_vals()
        res = super().write(vals)
        return res

    def _refresh_products_vals(self):
        """Reapply profile values on products"""
        for rec in self:
            products = self.env["product.product"].search([("profile_id", "=", rec.id)])
            if products:
                _logger.info(
                    " >>> %s Products updating after updated '%s' pro"
                    "duct profile" % (len(products), rec.name)
                )
                data = products._get_vals_from_profile(
                    {"profile_id": rec.id}, ignore_defaults=True
                )
                products.write(data)

    @api.model
    def check_useless_key_in_vals(self, vals, key):
        """If replacing values are the same than in db, we remove them.
        Use cases:
        1/ if in edition mode you switch a field
           from value A to value B and then go back to value A
           then save form, field is in vals whereas it shouldn't.
        2/ if profile data are in csv file there are processed
           each time module containing csv is loaded
        we remove field from vals to minimize impact on products
        """
        comparison_value = self[key]
        if self._fields[key].type == "many2one":
            comparison_value = self[key].id
        elif self._fields[key].type == "many2many":
            comparison_value = [
                (6, False, self[key].ids),
            ]
        return vals[key] == comparison_value

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """ Display a warning for end user if edit record """
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        if view_type == "form":
            style = "alert alert-warning oe_text_center oe_edit_only"
            alert = etree.Element("h2", {"class": style})
            alert.text = _(
                "If you update this profile, all products "
                "using this profile could also be updated. "
                "Changes can take a while."
            )
            doc = etree.XML(res["arch"])
            doc[0].addprevious(alert)
            res["arch"] = etree.tostring(doc, pretty_print=True)
        return res


class ProductMixinProfile(models.AbstractModel):
    _name = "product.mixin.profile"
    _description = "Product Profile Mixin"

    @api.model
    def _get_profile_fields(self):
        fields_to_exclude = set(get_profile_fields_to_exclude())
        return [
            field
            for field in self.env["product.profile"]._fields.keys()
            if field not in fields_to_exclude
        ]

    @api.model
    def _get_vals_from_profile(self, product_values, ignore_defaults=False):
        res = {}
        profile_obj = self.env["product.profile"]
        fields = self._get_profile_fields()
        profile_vals = profile_obj.browse(product_values["profile_id"]).read(fields)[0]
        profile_vals.pop("id")
        profile_vals = self._reformat_relationals(profile_vals)
        for key, val in profile_vals.items():
            if key[:LEN_DEF_STR] == PROF_DEFAULT_STR:
                if not ignore_defaults:
                    destination_field = key[LEN_DEF_STR:]
                    res[destination_field] = val
            else:
                res[key] = val
        return res

    def _reformat_relationals(self, profile_vals):
        res = deepcopy(profile_vals)
        profile_obj = self.env["product.profile"]
        for key, value in profile_vals.items():
            if value and profile_obj._fields[key].type == "many2one":
                # m2o value is a tuple
                res[key] = value[0]
            if profile_obj._fields[key].type == "many2many":
                res[key] = [(6, 0, value)]
        return res

    @api.onchange("profile_id")
    def _onchange_from_profile(self):
        """ Update product fields with product.profile corresponding fields """
        self.ensure_one()
        if self.profile_id:
            ignore_defaults = True if self._origin.profile_id else False
            values = self._get_vals_from_profile(
                {"profile_id": self.profile_id.id},
                ignore_defaults=ignore_defaults,
            )
            for field, value in values.items():
                try:
                    self[field] = value
                except Exception as e:
                    raise UserError(format_except_message(e, field, self))

    @api.model
    def create(self, vals):
        if vals.get("profile_id"):
            vals.update(self._get_vals_from_profile(vals, ignore_defaults=False))
        return super().create(vals)

    def write(self, vals):
        profile_changed = vals.get("profile_id")
        if profile_changed:
            recs_has_profile = self.filtered(lambda r: r.profile_id)
            recs_no_profile = self - recs_has_profile
            recs_has_profile.write(
                self._get_vals_from_profile(vals, ignore_defaults=True)
            )
            recs_no_profile.write(
                self._get_vals_from_profile(vals, ignore_defaults=False)
            )
        return super().write(vals)

    @api.model
    def _get_default_profile_fields(self):
        " Get profile fields with prefix PROF_DEFAULT_STR "
        return [
            x
            for x in self.env["product.profile"]._fields.keys()
            if x[:LEN_DEF_STR] == PROF_DEFAULT_STR
        ]

    @api.model
    def _customize_view(self, res, view_type):
        profile_group = self.env.ref("product_profile.group_product_profile_user")
        users_in_profile_group = [user.id for user in profile_group.users]
        default_fields = self._get_default_profile_fields()
        if view_type == "form":
            doc = etree.XML(res["arch"])
            fields = self._get_profile_fields()
            if self.env.uid not in users_in_profile_group:
                attrs = {"invisible": [("profile_id", "!=", False)]}
            else:
                attrs = {"readonly": [("profile_id", "!=", False)]}
            paths = ["//field[@name='%s']", "//label[@for='%s']"]
            for field in fields:
                if field not in default_fields:
                    # default fields shouldn't be modified
                    for path in paths:
                        node = doc.xpath(path % field)
                        if node:
                            for current_node in node:
                                current_node.set("attrs", str(attrs))
            res["arch"] = etree.tostring(doc, pretty_print=True)
        elif view_type == "search":
            # Allow to dynamically create search filters for each profile
            filters_to_create = self._get_profiles_to_filter()
            doc = etree.XML(res["arch"])
            node = doc.xpath("//filter[1]")
            if node:
                for my_filter in filters_to_create:
                    elm = etree.Element(
                        "filter", **self._customize_profile_filters(my_filter)
                    )
                    node[0].addprevious(elm)
                res["arch"] = etree.tostring(doc, pretty_print=True)
        return res

    @api.model
    def _get_profiles_to_filter(self):
        """ Inherit if you want that some profiles doesn't have a filter """
        return [(x.id, x.name) for x in self.env["product.profile"].search([])]

    @api.model
    def _customize_profile_filters(self, my_filter):
        """ Inherit if you to customize search filter display"""
        return {
            "string": "%s" % my_filter[1],
            "help": "Filtering by Product Profile",
            "domain": "[('profile_id','=', %s)]" % my_filter[0],
        }
