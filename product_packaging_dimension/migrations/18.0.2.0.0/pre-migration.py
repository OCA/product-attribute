# Copyright (C) 2026 Your Name / Company
# License AGPL-3.0 or later (http://gnu.org).

from openupgradelib import openupgrade


def migrate(cr, version):
    """Safely cast dimension columns to float for version 18.0.2.0.0."""
    openupgrade.logged_query(
        cr,
        """
        ALTER TABLE product_packaging
        ALTER COLUMN height TYPE double precision
        USING height::double precision
        """,
    )

    openupgrade.logged_query(
        cr,
        """
        ALTER TABLE product_packaging
        ALTER COLUMN width TYPE double precision
        USING width::double precision
        """,
    )

    openupgrade.logged_query(
        cr,
        """
        ALTER TABLE product_packaging
        ALTER COLUMN packaging_length TYPE double precision
        USING packaging_length::double precision
        """,
    )
