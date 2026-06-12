# Copyright 2025 Juan Carlos Oñate - Tecnativa <juancarlos.onate@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import time

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

API_URL = "https://eprel.ec.europa.eu/"


class ProductTemplate(models.Model):
    _inherit = "product.template"

    eprel_enabled = fields.Boolean(
        string="EPREL Enabled", compute="_compute_eprel_enabled"
    )
    eprel_model_identifier = fields.Char(string="Model Identifier", copy=False)
    eprel_energy_class_image = fields.Char(string="Energy Class Image", copy=False)
    fiche_url = fields.Char(
        compute="_compute_eprel_url", string="Fiche URL", readonly=True, store=True
    )
    label_url = fields.Char(
        compute="_compute_eprel_url", string="Label URL", readonly=True, store=True
    )
    label_arrow_url = fields.Char(
        compute="_compute_eprel_url",
        string="Label Arrow URL",
        readonly=True,
        store=True,
    )
    eprel_registration_number = fields.Char(
        string="EPREL Registration Number",
        copy=False,
        help="The EPREL registration number fetched from the API.",
    )

    def _compute_eprel_enabled(self):
        for rec in self:
            rec.eprel_enabled = bool(rec.env.company.eprel_api_key)

    @api.depends("categ_id.eprel_category_id", "eprel_registration_number")
    def _compute_eprel_url(self):
        for rec in self:
            cat = rec.categ_id.eprel_category_id.code
            reg_num = rec.eprel_registration_number
            arrow_image_name = (
                rec.eprel_energy_class_image.replace(".svg", ".png")
                if rec.eprel_energy_class_image
                and isinstance(rec.eprel_energy_class_image, str)
                else False
            )
            lang_code = self.env.company.partner_id.lang.split("_")[0]
            rec.fiche_url = (
                f"{API_URL}fiches/{cat}/Fiche_{reg_num}_{lang_code.upper()}.pdf"
                if cat and reg_num
                else False
            )
            rec.label_url = (
                f"{API_URL}labels/{cat}/Label_{reg_num}.png"
                if cat and reg_num
                else False
            )
            rec.label_arrow_url = (
                "https://ec.europa.eu/assets/move-ener/eprel/"
                f"EPREL%20Public/Nested-labels%20thumbnails/{arrow_image_name}"
                if arrow_image_name
                else False
            )

    def action_get_eprel_registration_number(self):
        if not self.env.company.eprel_api_key:
            raise UserError(_("EPREL API Key is not configured."))
        min_interval = 0.25
        last_request_time = 0.0
        for product in self:
            # Delay control to respect the API rate limit
            now = time.time()
            elapsed = now - last_request_time
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            if (
                not product.eprel_model_identifier
                or not product.categ_id.eprel_category_id
            ):
                raise UserError(_("Model Identifier and EPREL Category must be set."))
            identifier = product.eprel_model_identifier
            category_code = product.categ_id.eprel_category_id.code
            data = self._request_eprel_data(identifier, category_code)
            last_request_time = time.time()
            if data.get("hits"):
                product.eprel_registration_number = data.get("hits")[0].get(
                    "eprelRegistrationNumber"
                )
                product.eprel_energy_class_image = data.get("hits")[0].get(
                    "energyClassImage"
                )

    @api.model
    def _get_eprel_registration_number(self):
        products = self.search(
            [
                ("eprel_model_identifier", "!=", False),
                ("categ_id.eprel_category_id", "!=", False),
            ]
        )
        products.action_get_eprel_registration_number()

    def _request_eprel_data(self, identifier, category_code):
        url = f"{API_URL}api/products/{category_code}?modelIdentifier={identifier}"
        headers = {
            "X-API-KEY": self.env.company.eprel_api_key,
            "Accept": "application/json",
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise UserError(_("Failed to fetch EPREL data: %s") % str(e))
