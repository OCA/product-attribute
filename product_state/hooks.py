from openupgradelib.openupgrade import logged_query


def post_init_hook(env):
    """This hook is used to add a state on existing products
    when module product_state is installed.
    Using direct SQL query to avoid computational overhead.
    """
    logged_query(env.cr, """
        UPDATE product_template
        SET state = 'sellable',
        product_state_id = (
            SELECT id FROM product_state WHERE code = 'sellable' LIMIT 1
        )
        WHERE state IS NULL;
    """)
