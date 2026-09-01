# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Category — HS Code Mapping",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "summary": (
        "Map customs HS codes to Odoo product categories. Used by EDI / "
        "supplier integrations to auto-categorise newly imported products."
    ),
    "author": "Bosd, Odoo Community Association (OCA)",
    "maintainers": ["bosd"],
    "website": "https://github.com/OCA/product-attribute",
    "development_status": "Beta",
    "depends": [
        # ``stock_delivery`` is the OCB module that defines
        # ``product.template.hs_code`` in v19. The matcher is
        # conceptually about HS codes, so depending on the
        # canonical source is honest. Pulls in ``sale_stock`` +
        # ``delivery`` transitively — the cost on most installs
        # is zero (Inventory + Shipping are usually present
        # already in any Odoo deployment that handles physical
        # goods).
        "stock_delivery",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_hs_mapping.xml",
        "views/menus.xml",
        "data/server_action_recategorise.xml",
    ],
}
