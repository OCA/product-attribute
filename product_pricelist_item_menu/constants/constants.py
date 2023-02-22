from odoo import _

PRODUCT_LENGTH = "product_length"
PRODUCT_WIDTH = "product_width"
PRODUCT_HEIGHT = "product_height"
PRODUCT_AREA_WH = "product_area_wh"
PRODUCT_VOLUME = "product_volume"

DIMENSION_SELECTION = [
    (PRODUCT_LENGTH, _("Length")),
    (PRODUCT_WIDTH, _("Width")),
    (PRODUCT_HEIGHT, _("Height")),
    (PRODUCT_AREA_WH, _("Area W*H")),
    (PRODUCT_VOLUME, _("Volume")),
]

DIMENSIONS_BASE_UOM = {
    PRODUCT_LENGTH: "product_pricelist_items_menu.product_uom_mm",
    PRODUCT_WIDTH: "product_pricelist_items_menu.product_uom_mm",
    PRODUCT_HEIGHT: "product_pricelist_items_menu.product_uom_mm",
    PRODUCT_AREA_WH: "product_pricelist_items_menu.product_uom_m2",
    PRODUCT_VOLUME: "uom.product_uom_cubic_meter",
}


def dimensions_base_uom_ids(env):
    base_uom_ids = {
        dimension: env.ref(DIMENSIONS_BASE_UOM[dimension])
        for dimension in DIMENSIONS_BASE_UOM
    }
    return base_uom_ids


LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT = [
    dimension for dimension in DIMENSIONS_BASE_UOM
]

FIXED_PRICE_TYPE = "f"

PRICE_TYPE_SELECTION = [(FIXED_PRICE_TYPE, "Fixed")] + [
    dimension_selction for dimension_selction in DIMENSION_SELECTION
]


def check_dim_vals(dim_vals):
    """
    Some methods may be passing not all dimensions so we need to compute them
    :param: dim_vals : dictitionary : dimensions with values
    """
    if dim_vals.get(PRODUCT_AREA_WH, 0) == 0:
        product_length = dim_vals.get(PRODUCT_LENGTH, 0)
        if product_length == "":
            product_length = 0.0
        product_height = dim_vals.get(PRODUCT_HEIGHT, 0)
        if product_height == "":
            product_height = 0.0
        product_width = dim_vals.get(PRODUCT_WIDTH, 0)
        if product_width == "":
            product_width = 0.0
        if PRODUCT_HEIGHT in dim_vals and PRODUCT_WIDTH in dim_vals:
            product_area_wh = product_height * product_width / 1000000
            dim_vals.update({PRODUCT_AREA_WH: product_area_wh})
    return dim_vals


def match_value(value, value_from, value_to):
    """
    Checks if value matches criteria
    :param Float value: Value
    :param value_from: -- from
    :param value_to:  -- to
    :return: True if matches else False
    """
    # equal
    if value_from == value_to == value:
        return True
    # between
    elif 0 < value_from < value and value_to > 0 and value < value_to:
        return True
    # <
    elif value_from == 0 and value < value_to:
        return True
    # >
    elif value_to == 0 and value > value_from:
        return True
    # miss
    return False


TOKEN_PATTERN = r"[a-zA-Z._0-9]+|[=+\-\/*()]"

PRICELIST_ITEM_MINIMAL_FROM = 1
