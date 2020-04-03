# Copyright 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from . import common

from ..tablib import Tab


class TestTab(common.TestCommon):

    def test_create_page(self):
        self.assertTrue(bool(self.tab_installation_services))
        tab_obj = Tab(self.tab_installation_services)
        page = tab_obj.create_page()
        # And we should have a field for (amongst others) selection_type_id.
        field = page.xpath('//field[@name="type_selection_id"]')
        self.assertTrue(field, 'Field selection_type_id not in page.')

    def test_visibility(self):
        """Tab positions should be shown for functionaries, but not others."""
        self.assertTrue(bool(self.tab_supported_machines))
        self.assertTrue(bool(self.product_basic_is))
        self.assertTrue(bool(self.product_premius_ss))
        tab_obj = Tab(self.tab_supported_machines)
        self.assertTrue(
            tab_obj.compute_visibility(self.product_basic_is),
            'Positions tab should be visible for functionary.')
        self.assertFalse(
            tab_obj.compute_visibility(self.product_premius_ss),
            'Positions tab should not be visible for non-functionary.')
        # Tab for departments should only be visible for main product
        self.assertTrue(bool(self.tab_spares))
        self.assertTrue(bool(self.product_machine))
        tab_obj = Tab(self.tab_spares)
        self.assertTrue(
            tab_obj.compute_visibility(self.env.ref('base.main_product')),
            'Department tab should be visible for main product.')
        self.assertFalse(
            tab_obj.compute_visibility(self.product_machine),
            'Department tab should not be visible for other products.')
