# Copyright 2021 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)


def make_pkg_values(product, record, **kw):
    """Helper to generate test values for packaging.

    `record` is a `uom.uom`: the product's own UoM (minimal unit) or one of
    its packaging UoMs (`product.uom_ids`).
    """
    is_unit = record == product.uom_id
    if is_unit:
        qty = product.uom_id.factor
        barcode = None
        name = record.name
    else:
        qty = record._compute_quantity(1, product.uom_id, round=False)
        barcode = product._packaging_barcode(record)
        name = product._packaging_name_getter(record)
    values = {
        "id": record.id,
        "name": name,
        "qty": qty,
        "barcode": barcode,
        "is_unit": is_unit,
    }
    values.update(kw)
    return values
