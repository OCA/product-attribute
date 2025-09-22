# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
    battery_capacity = fields.Char(string="Battery Capacity mWh")
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
