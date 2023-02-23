# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class StockLotArchive(models.TransientModel):

    _name = "stock.lot.archive"
    _description = "Stock Lot Archive"

    @api.model
    def _archive_lots(self) -> None:
        """
        A product can have a lot of lots. To avoid this problem we archive old lot.
        Archive a lot has not effect (we don't use the 'active' field).

        We archive a lot if and only if:
        - There are no more products in this lot
        - There is a new lot (with a higher expiration date) for this product

        :return:
        """
        query = """
            SELECT lot.id
            FROM stock_lot AS lot
            WHERE (lot.is_archived = False OR lot.is_archived IS NULL)
            AND EXISTS (SELECT 1
                          FROM stock_lot AS next_lot
                          WHERE next_lot.product_id = lot.product_id
                          AND next_lot.expiration_date >= lot.expiration_date
                          AND next_lot.id <> lot.id)
            AND NOT EXISTS (SELECT 1
                            FROM stock_quant AS quant
                            JOIN stock_location sl on sl.id = quant.location_id
                            WHERE quant.lot_id = lot.id AND sl.usage = 'internal'
                            AND sl.parent_path LIKE ANY(%(location_paths)s)
                            );
            """
        location_paths = (
            self.env["stock.warehouse"]
            .search([])
            .mapped("view_location_id.parent_path")
        )
        params = {
            "location_paths": [
                "{}%".format(location_path) for location_path in location_paths
            ]
        }
        self.env.cr.execute(query, params)

        result = self.env.cr.fetchall()
        lot_to_archive_ids = [lot[0] for lot in result]

        self.env["stock.lot"].browse(lot_to_archive_ids).write({"is_archived": True})
