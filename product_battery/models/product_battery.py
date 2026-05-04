# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductBattery(models.Model):
    _name = "product.battery"

    product_tmpl_id = fields.Many2one("product.template")
    battery_type = fields.Selection(
        [
            ("primary", "Primary (non-rechargeable)"),
            ("secondary", "Secondary (rechargeable)"),
        ],
    )
    battery_qty = fields.Integer(string="Quantity")
    battery_chemistry = fields.Selection(
        [
            ("alkaline", "Alkaline (Zn/MnO2)"),
            ("nickel_cadmium", "Nickel-Cadmium (Ni/Cd)"),
            ("nickel_metal_hydride", "Nickel-Metal Hydride (Ni/MH)"),
            ("lithium_cobalt_oxide", "Lithium Cobalt Oxide (LiCoO2)"),
            ("lithium_polymer", "Lithium Polymer"),
            ("lead_acid", "Lead-Acid (Pb/PbO2)"),
            ("lithium_iron_phosphate", "Lithium Iron Phosphate (LiFePO4)"),
            ("zinc_carbon", "Zinc-Carbon (Zn/C)"),
            ("silver_oxide", "Silver Oxide (Ag2O)"),
            ("mercury_oxide", "Mercury Oxide (HgO)"),
            ("sodium_sulfur", "Sodium-Sulfur (Na/S)"),
        ],
    )
    battery_form = fields.Selection(
        [
            ("cylindrical", "Cylindrical"),
            ("prismatic", "Prismatic"),
            ("pouch", "Pouch"),
            ("button_cell", "Button Cell Small"),
            ("square", "Square"),
            ("lead-acid", "Lead-Acid"),
            (
                "pack",
                "Pack",
            ),
        ],
    )
    battery_weight = fields.Float(string="Battery Weight in Grams")
    battery_charge_capacity = fields.Float(string="Battery Charge Capacity (mAh)")
    battery_capacity = fields.Float(
        string="Battery Capacity mWh",
        compute="_compute_battery_capacity",
        store="True",
        digits=(16, 2),
    )
    battery_voltage = fields.Float(string="Battery Voltage (V)")
    battery_removable = fields.Selection(
        [
            ("yes", "Yes"),
            (
                "no",
                "No",
            ),
        ],
        string="Removable",
    )
    battery_manufacture = fields.Char(string="Manufacture")
    reference_to_battery_product = fields.Char("Internal Reference")
    regulatory_category = fields.Selection(
        [
            (
                "portable",
                "Portable",
            ),
            (
                "lmt",
                "LMT",
            ),
            ("industrial", "Industrial"),
            ("ev", "EV"),
            ("sli", "SLI"),
        ],
    )
    lead_exceed = fields.Boolean(string="Exceeds Lead by 0.004%")
    cadmium_exceed = fields.Boolean(string="Exceeds Cadmium by 0.002%")
    mercury_exceed = fields.Boolean(string="Exceeds Mercury by 0.0005%")

    @api.depends("battery_charge_capacity", "battery_voltage")
    def _compute_battery_capacity(self):
        for record in self:
            if record.battery_voltage != 0:
                record.battery_capacity = (
                    (record.battery_charge_capacity / 1000) * record.battery_voltage
                )
            else:
                record.battery_capacity = 0
