from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sequences = (
        env["product.template"]
        .search(
            [
                ("lot_sequence_id.code", "=", False),
                ("lot_sequence_id", "!=", False),
            ]
        )
        .mapped("lot_sequence_id")
    )
    if sequences:
        sequences.write({"code": "product_lot_sequence"})
