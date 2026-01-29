# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

BATCH_SIZE = 2000


def post_init_hook(env):
    lang_codes = env["res.lang"].search([("active", "=", True)]).mapped("code")
    Product = env["product.product"]
    product_ids = Product.search([]).ids
    if not product_ids:
        return
    for lang in lang_codes:
        for i in range(0, len(product_ids), BATCH_SIZE):
            batch_ids = product_ids[i : i + BATCH_SIZE]
            recs = Product.browse(batch_ids).with_context(lang=lang)
            recs._compute_variant_search_text()
