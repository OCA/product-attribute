# copyright David BEAL @ Akretion


def pre_init_hook(env):
    # Rename the "Product Manager" group to a more matching name
    # and avoid collision with current module
    env.ref("product.group_product_manager").name = "Product Manager"
