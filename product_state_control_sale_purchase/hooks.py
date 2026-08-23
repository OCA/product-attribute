def post_init_hook(env):
    update_product_states(env)


def update_product_states(env):
    mapping = {
        "product_state.product_state_draft": {
            "authorized_to_be_sold": False,
            "authorized_to_be_bought": False,
        },
        "product_state.product_state_sellable": {
            "authorized_to_be_sold": True,
            "authorized_to_be_bought": True,
        },
        "product_state.product_state_end": {
            "authorized_to_be_sold": False,
            "authorized_to_be_bought": True,
        },
        "product_state.product_state_obsolete": {
            "authorized_to_be_sold": False,
            "authorized_to_be_bought": True,
        },
    }

    for xml_id, values in mapping.items():
        state = env.ref(xml_id, raise_if_not_found=False)
        if state:
            state.write(values)
