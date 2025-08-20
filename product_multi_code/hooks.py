# © 2025 Valentin Vinagre (Sygel)
# © 2025 Ángel Rivas (Sygel)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init_hook(env):
    Product = env["product.product"]

    for product in Product.search([]):
        if not product.default_code:
            continue
        env.cr.execute(
            """
            SELECT 1 FROM product_default_code
            WHERE product_id = %s AND name = %s
        """,
            (product.id, product.default_code),
        )
        if env.cr.fetchone():
            continue
        env.cr.execute(
            """
            INSERT INTO product_default_code
                (product_id, product_tmpl_id, name, sequence)
            VALUES (%s, %s, %s, %s)
        """,
            (
                product.id,
                product.product_tmpl_id.id,
                product.default_code,
                0,
            ),
        )


def uninstall_hook(env):
    env.cr.execute(
        """
        UPDATE product_product pp
        SET default_code = pp.default_code
    """
    )
    env.cr.execute("DELETE FROM product_default_code")
